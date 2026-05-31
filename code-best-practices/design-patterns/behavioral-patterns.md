# Behavioral Patterns

## Strategy

- A strategy is a way to swap one behavior for another.
- Use it when you have several ways to do the same job.
- It is often better than a large `if/else` block that switches by type or mode.

Good examples:

- pricing strategies
- discount rules
- shipping cost calculation

Simple example:

```ts
const pricing = pricingStrategy.calculate(order);
```

- `HolidayPricingStrategy` and `StandardPricingStrategy` can both follow the same contract.

Code example:

```ts
interface PricingStrategy {
  calculate(order: Order): number;
}

class StandardPricingStrategy implements PricingStrategy {
  calculate(order: Order): number {
    return order.total;
  }
}

class VipPricingStrategy implements PricingStrategy {
  calculate(order: Order): number {
    return order.total * 0.9;
  }
}

const strategy: PricingStrategy = new VipPricingStrategy();
const total = strategy.calculate(order);
```

- The calling code uses the same `calculate()` method, but the pricing rule can change.

Avoid:

- creating a full strategy hierarchy when there are only two trivial cases and no likely growth

## Observer

- Observer means one thing changes and other parts can react to it.
- Use it when several listeners should respond without being tightly wired into the source object.
- It works well for events, notifications, and decoupled reactions.

Good examples:

- `OrderPaid` event triggering email, analytics, and fulfillment

Simple example:

```ts
eventBus.publish(new OrderPaid(orderId));
```

- Email, analytics, and fulfillment handlers can all listen without `OrderService` calling each one directly.

Code example:

```ts
interface WeatherObserver {
  update(temperature: number): void;
}

class PhoneDisplay implements WeatherObserver {
  update(temperature: number): void {
    console.log(`phone shows ${temperature}`);
  }
}

class WindowDisplay implements WeatherObserver {
  update(temperature: number): void {
    console.log(`window shows ${temperature}`);
  }
}

class WeatherStation {
  private observers: WeatherObserver[] = [];

  subscribe(observer: WeatherObserver): void {
    this.observers.push(observer);
  }

  setTemperature(temperature: number): void {
    for (const observer of this.observers) {
      observer.update(temperature);
    }
  }
}

const station = new WeatherStation();
station.subscribe(new PhoneDisplay());
station.subscribe(new WindowDisplay());
station.setTemperature(22);
```

- When the weather changes, the station tells every subscribed display.

## Command

- A command turns an action into an object.
- Use it when you want to queue, retry, log, or delay an action.
- It helps when actions need a standard `execute()` shape.

Good examples:

- `SendInvoiceCommand`
- `RetryPaymentCommand`

Simple example:

```ts
queue.push(new SendInvoiceCommand(invoiceId));
```

- The queue stores the action as data and can run it later.

Code example:

```ts
interface Command {
  execute(): void;
}

class TurnOnLightCommand implements Command {
  execute(): void {
    console.log("light turned on");
  }
}

class Button {
  constructor(private readonly command: Command) {}

  click(): void {
    this.command.execute();
  }
}

const button = new Button(new TurnOnLightCommand());
button.click();
```

- The button does not know how to turn on the light. It just runs the command it was given.

## Template Method

- Template method means one class defines the main steps of a process, and child classes customize only some of those steps.
- Use it when the overall flow stays the same, but a few parts need to change.
- Prefer composition first if inheritance would make the design too rigid.

Simple example:

- a report generator where every report follows `load -> format -> export`, but each report type fills in different details

Code example:

```ts
abstract class ReportGenerator {
  generate(): void {
    const data = this.loadData();
    const content = this.format(data);
    this.export(content);
  }

  protected abstract loadData(): string[];
  protected abstract format(data: string[]): string;

  protected export(content: string): void {
    console.log(`export: ${content}`);
  }
}

class SalesReportGenerator extends ReportGenerator {
  protected loadData(): string[] {
    return ["sale1", "sale2"];
  }

  protected format(data: string[]): string {
    return `sales report: ${data.join(", ")}`;
  }
}

const report = new SalesReportGenerator();
report.generate();
```

- `generate()` always follows the same steps.
- The child class changes only `loadData()` and `format()`.
- That is the pattern: keep the main workflow fixed, customize only a few parts.

## Iterator

- An iterator gives you a simple way to go through a collection one item at a time.
- Use it when callers should be able to loop through items without knowing how they are stored.
- It helps hide whether the data comes from an array, a tree, paged results, or some custom structure.

Good examples:

- looping through paged API results
- walking nodes in a tree
- reading rows from a custom result set

Simple example:

```ts
for (const invoice of invoiceCollection) {
  sendReminder(invoice);
}
```

- The caller just loops over invoices and does not need to know whether they came from one list or several pages behind the scenes.

Code example:

```ts
class InvoiceCollection {
  constructor(private readonly invoices: string[]) {}

  [Symbol.iterator](): Iterator<string> {
    let index = 0;
    const invoices = this.invoices;

    return {
      next(): IteratorResult<string> {
        if (index < invoices.length) {
          return { value: invoices[index++], done: false };
        }

        return { value: undefined, done: true };
      },
    };
  }
}

const invoices = new InvoiceCollection(["inv-1", "inv-2"]);

for (const invoice of invoices) {
  console.log(invoice);
}
```

- The loop works the same way as with an array, even though the collection controls how items are returned.

Avoid:

- adding a custom iterator when a plain array loop is already enough

## Practical Checks

- Am I replacing repeated conditionals with something clearer?
- Does this pattern make behavior easier to extend without spreading `if/else` logic?
- Would a simple function map or small composition solve this more directly?
