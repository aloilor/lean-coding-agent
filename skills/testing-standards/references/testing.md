# Testing Strategy

## Match The Repo's Existing Test Setup

A test only helps if it fits the project it lands in. Before writing anything, discover the existing setup and conform to it — a Jest file dropped into a Vitest/pytest/Go suite, tests placed in the wrong directory, or a new naming scheme all create friction and often won't even run.

**Discover, in order:**

1. **`agent-context/testing.md`** — the project's documented test commands, expectations, and fixture conventions. When it exists, it is the source of truth.
2. **The repo itself** — to confirm the docs and fill gaps. Look for:

| What to find | Why it matters |
|--------------|----------------|
| Framework and runner | Determines syntax, structure, and how doubles work. |
| Run command (incl. single-file/filtered) | You need to run the narrowest test fast during the loop. |
| Test file location and naming | New tests must sit where the suite discovers them. |
| Assertion style | Match `expect`, `assert`, table-driven, etc. |
| Mocking / fixture approach | Reuse the established double and setup style. |
| Existing builders, factories, fixtures, helpers | Reuse them instead of inventing parallel ones. |

**Then mirror it.** Place new tests alongside existing ones, name them the project's way, and use the established assertion and double styles. Reuse existing fixtures and builders before adding new ones.

**Only deviate deliberately.** Introduce a new framework, layout, or convention only when the task explicitly requires it. If the repo has no test setup at all, propose the smallest reasonable one and flag the choice rather than silently establishing a precedent.

---

## The Testing Pyramid

```
       /\
      /  \        E2E Tests (Few)
     /----\       - Full system
    /      \      - Slow, brittle
   /--------\
  /          \    Integration Tests (Some)
 /------------\   - Multiple components
/              \  - Medium speed
----------------
      Unit Tests (Many)
      - Single unit
      - Fast, isolated
```

## Test Types

### Unit Tests

Test ONE class or function in isolation.

**Characteristics:**
- Fast (milliseconds)
- No external dependencies (mocked)
- Most of your tests should be unit tests

```typescript
describe('Order', () => {
  it('calculates total correctly', () => {
    const order = new Order();
    order.addItem({ price: 100 });
    order.addItem({ price: 50 });

    expect(order.calculateTotal()).toBe(150);
  });
});
```

### Integration Tests

Test multiple components together.

**Characteristics:**
- Slower (may use real DB)
- Test boundaries between components
- Fewer than unit tests

```typescript
describe('OrderService Integration', () => {
  let db: Database;
  let service: OrderService;

  beforeAll(async () => {
    db = await Database.connect();
    service = new OrderService(new PostgresOrderRepo(db));
  });

  it('saves and retrieves an order', async () => {
    const order = Order.create({ customerId: '123' });
    await service.save(order);

    const retrieved = await service.findById(order.id);
    expect(retrieved).toEqual(order);
  });
});
```

### E2E / Acceptance Tests

Test the entire system from user perspective.

**Characteristics:**
- Slowest
- Most brittle (many moving parts)
- Test critical paths only

```typescript
describe('Checkout Flow', () => {
  it('user can complete purchase', async () => {
    await page.goto('/products');
    await page.click('[data-testid="add-to-cart"]');
    await page.click('[data-testid="checkout"]');
    await page.fill('[name="card"]', '4242424242424242');
    await page.click('[data-testid="pay"]');

    expect(await page.textContent('h1')).toBe('Order Confirmed');
  });
});
```

---

## Arrange-Act-Assert And Test Naming

See `SKILL.md` for the Arrange-Act-Assert structure and concrete-behavior naming guidance that applies to every test below.

---

## Test Doubles

### Dummy

Object passed but never used.

```typescript
const dummyLogger = {} as Logger;
new UserService(realRepo, dummyLogger);
```

### Stub

Returns predefined values.

```typescript
const stubRepo: UserRepo = {
  findById: () => Promise.resolve(new User({ name: 'Test' })),
  save: () => Promise.resolve(),
};
```

### Spy

Records how it was called.

```typescript
const emailSpy = {
  sentEmails: [] as string[],
  send(to: string, message: string) {
    this.sentEmails.push(to);
  }
};

// Later
expect(emailSpy.sentEmails).toContain('user@example.com');
```

### Mock

Verifies expected interactions.

```typescript
const mockRepo = { save: jest.fn().mockResolvedValue(undefined) } as jest.Mocked<UserRepo>;

// After test
expect(mockRepo.save).toHaveBeenCalledWith(expectedUser);
```

### Fake

Working implementation (simplified).

```typescript
class InMemoryUserRepo implements UserRepo {
  private users: Map<string, User> = new Map();

  async save(user: User): Promise<void> {
    this.users.set(user.id, user);
  }

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) || null;
  }
}
```

---

## Make Hard-To-Test Code Testable

If a behavior is hard to test, that is a design signal, not a reason to skip the test. The usual cause is logic buried in a side effect or reaching for a hidden dependency. Create a seam and test through it:

- **Inject the dependency.** Pass the clock, database, HTTP client, mailer, or random source in as an argument instead of constructing or importing it inside the unit. Now a test can supply a fake or stub.
- **Return a value instead of only performing an effect.** A function that computes and returns a result is trivially testable; one that only writes to a file, log, or queue forces you to test the effect.
- **Surface the effect.** When the effect *is* the behavior (an email must be sent), route it through an injected collaborator you can spy on, or emit an observable result/event, rather than firing it deep inside.
- **Separate decision from action.** Pull the logic (what to do) out of the I/O (doing it). Unit-test the decision as a pure function; keep a thin I/O wrapper for a small integration test.

```typescript
// Hard to test: reads the clock and sends email internally
async function expireTrial(userId: string) {
  const user = await db.users.find(userId);
  if (Date.now() > user.trialEndsAt) {
    await sendgrid.send(user.email, 'Trial expired');
  }
}

// Testable: decision is pure, dependencies are injected
function isTrialExpired(user: User, now: number): boolean {
  return now > user.trialEndsAt;            // unit-test this directly
}

async function expireTrial(
  userId: string,
  deps: { now: () => number; mailer: Mailer; repo: UserRepo },
) {
  const user = await deps.repo.find(userId);
  if (isTrialExpired(user, deps.now())) {
    await deps.mailer.send(user.email, 'Trial expired');  // spy on this
  }
}
```

Prefer making the seam over testing private internals, monkeypatching globals, or asserting on log output. If you genuinely cannot make the behavior testable within the task's scope, say so and flag it — do not silently drop the test.

## Testing Strategies by Layer

### Domain Layer (Most Tests)

- Unit tests with no mocks
- Test business rules, value objects, entities
- Fast, comprehensive

```typescript
describe('Money', () => {
  it('adds amounts with same currency', () => {
    const a = Money.dollars(10);
    const b = Money.dollars(20);
    expect(a.add(b).equals(Money.dollars(30))).toBe(true);
  });

  it('throws when adding different currencies', () => {
    const usd = Money.dollars(10);
    const eur = Money.euros(10);
    expect(() => usd.add(eur)).toThrow(CurrencyMismatch);
  });
});
```

### Application Layer

- Integration tests with mocked infrastructure
- Test use case orchestration

```typescript
describe('CreateOrderUseCase', () => {
  it('creates order and sends confirmation', async () => {
    const orderRepo = new InMemoryOrderRepo();
    const emailService = { send: jest.fn() };
    const useCase = new CreateOrderUseCase(orderRepo, emailService);

    await useCase.execute({ customerId: '123', items: [...] });

    expect(orderRepo.count()).toBe(1);
    expect(emailService.send).toHaveBeenCalled();
  });
});
```

### Infrastructure Layer

- Integration tests with real dependencies
- Test database, API integrations

```typescript
describe('PostgresOrderRepo', () => {
  let repo: PostgresOrderRepo;

  beforeAll(async () => {
    repo = new PostgresOrderRepo(testDb);
  });

  it('persists and retrieves order', async () => {
    const order = Order.create({ ... });
    await repo.save(order);

    const found = await repo.findById(order.id);
    expect(found).toEqual(order);
  });
});
```

---

## High-Value Integration Tests

Focus integration tests on:

1. **Boundaries** - Where systems meet
2. **Critical paths** - Money, security, core features
3. **Complex queries** - Database operations

### Contract Tests

Verify implementations match interfaces.

```typescript
// Shared contract test
function testUserRepoContract(createRepo: () => UserRepo) {
  describe('UserRepo Contract', () => {
    let repo: UserRepo;

    beforeEach(() => {
      repo = createRepo();
    });

    it('saves and retrieves user', async () => {
      const user = User.create({ name: 'Test' });
      await repo.save(user);
      const found = await repo.findById(user.id);
      expect(found).toEqual(user);
    });

    it('returns null for missing user', async () => {
      const found = await repo.findById('nonexistent');
      expect(found).toBeNull();
    });
  });
}

// Apply to all implementations
testUserRepoContract(() => new InMemoryUserRepo());
testUserRepoContract(() => new PostgresUserRepo(testDb));
```

---

## Test Builders

Create test objects easily.

```typescript
class OrderBuilder {
  private props: Partial<OrderProps> = {
    id: 'order-1',
    customerId: 'cust-1',
    items: [],
    status: 'pending',
  };

  withId(id: string): OrderBuilder {
    this.props.id = id;
    return this;
  }

  withItems(items: Item[]): OrderBuilder {
    this.props.items = items;
    return this;
  }

  paid(): OrderBuilder {
    this.props.status = 'paid';
    return this;
  }

  build(): Order {
    return Order.create(this.props as OrderProps);
  }
}

// Usage
const order = new OrderBuilder()
  .withItems([{ sku: 'ABC', price: 100 }])
  .paid()
  .build();
```

---

## Reliability and Determinism

A flaky test erodes trust in the whole suite. Make tests pass or fail for one reason, every time.

### Isolate State

Reset or scope anything a test mutates: databases, queues, caches, files, module-level singletons.

```typescript
afterEach(async () => {
  await db.truncateAll();      // or wrap each test in a rolled-back transaction
});
```

- Prefer unique IDs, transactions, or disposable resources (temp dirs, ephemeral containers) over shared named records.
- No test should rely on another test running first, or on suite ordering.

### Control Time

Inject a clock; do not read the system time deep inside business logic.

```typescript
// Avoid: order.createdAt = new Date()  — reads the wall clock internally
const order = createOrder({ now: fixedClock.now() });
```

Test time zones, daylight-saving transitions, expiry windows, and clock skew when they affect behavior.

### Control Randomness

Fix the seed when randomness is part of the behavior under test, so a failure reproduces.

### Don't Sleep — Wait On Conditions

In async and end-to-end tests, wait for the state or event you expect, never an arbitrary delay. Fixed sleeps are the single most common source of flake and slowness.

```typescript
// Avoid: await sleep(2000)
await expect.poll(() => page.textContent('h1')).toBe('Order Confirmed');
```

### Run In Parallel Safely

Avoid shared ports, accounts, fixed filenames, or named records so the suite can parallelize without collisions.

### Use Safe, Realistic Data

- Fixtures should match production shapes, limits, encodings, and relationships, and include edge cases (empty strings, long strings, missing optional fields, time zones).
- Do not use production personal data unless it is legally allowed, minimized, and anonymized. Prefer synthetic fixtures.

---

## Common Testing Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Testing implementation | Brittle tests | Test behavior only |
| Too many mocks | Tests prove nothing | Use real objects when possible |
| Shared state | Flaky tests | Isolate each test |
| No assertions | False confidence | Always assert something meaningful |
| Testing trivial code | Wasted effort | Focus on logic and edge cases |
| Slow tests | Reduced feedback | Optimize, use unit tests |
