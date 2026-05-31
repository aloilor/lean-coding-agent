# Structural Patterns

## Adapter

- An adapter is a translator between two interfaces that do not match.
- Use it when your code expects one shape, but a library or old system gives you a different one.
- The adapter lets your app keep its own interface while translating calls to the outside system.

Good example:

- `StripePaymentGatewayAdapter` implementing your local `PaymentGateway` interface

Simple example:

```ts
const gateway = new StripePaymentGatewayAdapter(stripeClient);
gateway.charge(amount);
```

- Your app talks to `PaymentGateway`, not directly to the Stripe SDK.

What this means:

- Your app might expect a method like `charge(amount)`.
- The Stripe client might expose a different method name and different argument shape.
- The adapter sits in the middle and translates one into the other.

Concrete example:

```ts
interface PaymentGateway {
  charge(amount: number): Promise<void>;
}

class StripePaymentGatewayAdapter implements PaymentGateway {
  constructor(private readonly stripeClient: StripeClient) {}

  async charge(amount: number): Promise<void> {
    await this.stripeClient.pay({ totalInCents: amount * 100 });
  }
}
```

- The rest of your app can call `gateway.charge(50)`.
- Only the adapter needs to know that Stripe expects `pay({ totalInCents: 5000 })`.

More examples:

- `LegacyUserStoreAdapter` wrapping an old user API
- `MailchimpEmailSenderAdapter` implementing your local `EmailSender`
- `SlackNotifierAdapter` implementing your local `Notifier`

Avoid:

- letting Stripe, Mailchimp, or legacy API shapes leak directly into business logic

## Decorator

- A decorator wraps an object and adds behavior around it.
- Use it when you want to keep the original object but add things like logging, caching, retries, or metrics.
- It is often better than inheritance for this kind of extra behavior.

Good examples:

- `CachedUserReader`
- `LoggedMessageBus`
- `MeteredPaymentGateway`

Simple example:

```ts
const reader = new CachedUserReader(databaseUserReader);
```

- `CachedUserReader` still behaves like a `UserReader`, but adds caching around it.

More examples:

- `RetryingPaymentGateway`
- `AuthorizedDocumentStore`

## Facade

- A facade gives callers one simple entry point to a more complex subsystem.
- Use it when the real work needs many low-level calls that most callers should not know about.
- It helps hide orchestration details behind one clear API.

Good example:

- `checkoutService.completeOrder(orderId)` instead of making callers coordinate payment, inventory, invoicing, and email

Simple example:

```ts
checkoutService.completeOrder(orderId);
```

- The caller uses one method instead of coordinating payment, stock, invoice creation, and email directly.

More examples:

- `reportService.generateMonthlyReport(month)`
- `onboardingService.createEmployee(profile)`

## Proxy

- A proxy stands in front of another object and controls access to it.
- Use it when you want to add checks or delayed behavior before the real object is used.
- Common uses are lazy loading, authorization, remote access, and caching.

Simple example:

```ts
const store = new AuthorizedDocumentStore(realDocumentStore);
store.get(documentId);
```

- The proxy checks access before forwarding the call to the real store.

More examples:

- `LazyImageProxy`
- `CachedApiClientProxy`

## Practical Checks

- Am I hiding complexity or just moving it?
- Does this wrapper reduce coupling for callers?
- Would composition already solve this without naming a full pattern?
