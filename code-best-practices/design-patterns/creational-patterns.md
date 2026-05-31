# Creational Patterns

## Factory

- A factory is a place whose job is to create objects for you.
- Use it when creating the object is more than a simple `new Something(...)`.
- It helps when callers should ask for an object, not know all the steps to build it.

Good examples:

- `paymentGatewayFactory.create(provider)`
- `notificationSenderFactory.create(channel)`
- `storageClientFactory.create(environment)`
- `reportExporterFactory.create(format)`

Simple example:

```ts
const gateway = paymentGatewayFactory.create(provider);
```

- If `provider` is `"stripe"`, the factory can return `StripeGateway`.
- If `provider` is `"paypal"`, the factory can return `PaypalGateway`.
- The caller asks for a gateway, but does not need to know how each one is created.

Avoid:

- Adding a factory for a class that could just be created with `new UserService(...)`.

## Builder

- A builder helps you create one object step by step.
- Use it when the object has many optional parts or would need a long confusing constructor.
- It is useful when you want the final object to be created only after all needed parts are set.

Good examples:

- building a complex query
- building an email with optional attachments and headers
- building an HTTP request with optional headers, body, and timeout
- building a dashboard widget with optional filters and layout settings

Simple example:

```ts
const email = emailBuilder
  .to("a@example.com")
  .subject("Hello")
  .body("Hi")
  .addAttachment(file)
  .build();
```

- This is easier to read than one very long constructor.
- The final object is created only when `build()` is called.

Avoid:

- Using a builder for a simple object with two or three obvious fields.

## Singleton

- A singleton means there should be only one shared instance in the process.
- Be careful with it because it creates global state.
- Global state often makes testing and reasoning harder.
- Prefer dependency injection or explicit lifecycle management first.

Good use:

- one process-wide object only when the lifecycle is truly global and controlled
- one explicitly managed application logger shared across the process
- one controlled in-memory feature flag registry for the running process

Simple example:

- one shared logger used across the whole application
- one shared config registry loaded once at startup

- The key idea is not "make it global because it is convenient".
- The key idea is "there should truly be only one shared instance".

Avoid:

- using a singleton just to make access easy from anywhere

## Dependency Injection

- Dependency injection means an object receives the things it needs from the outside instead of creating them by itself.
- Use it when you want business code to stay separate from creation and wiring details.
- It makes testing easier because you can pass a fake or simpler implementation when needed.

Good examples:

- passing `PaymentGateway` into `OrderService`
- passing `UserRepository` into `UserService`
- passing `Clock` into time-based logic

Simple example:

```ts
class InvoiceService {
  constructor(private readonly gateway: InvoiceGateway) {}
}
```

- `InvoiceService` receives its dependency instead of creating `StripeGateway` or `PostgresGateway` by itself.
- This makes the service easier to test and easier to change later.

Avoid:

- creating dependencies directly inside business logic when they should be supplied from outside

```ts
class InvoiceService {
  private readonly gateway = new StripeGateway();
}
```

## Lazy Initialization

- Lazy initialization means you create something only when it is first needed.
- Use it when an object is expensive to create or may never be needed at all.
- It can save startup time or avoid unnecessary work.

Good examples:

- opening a database connection only when the first query runs
- creating a large report only when the user actually requests export
- loading a cache only when the first read happens

Simple example:

```ts
class ReportService {
  private exporter?: Exporter;

  getExporter() {
    if (!this.exporter) {
      this.exporter = new PdfExporter();
    }
    return this.exporter;
  }
}
```

- `PdfExporter` is created only when `getExporter()` is called for the first time.

Avoid:

- using lazy initialization for cheap objects when it only adds more branching and state to understand

## Prototype

- Prototype means creating a new object by copying an existing one.
- Use it when building a fresh object from scratch is harder than cloning a known good starting point.
- It is useful when you want a default template and then a few changes.

Good examples:

- cloning a default dashboard configuration and changing the filters
- copying a report template and changing the output format
- duplicating a game character or document template and customizing a few fields
- cloning a base test fixture and changing one or two fields
- copying a chart configuration and changing labels and data

Simple example:

```ts
const premiumInvoice = baseInvoiceTemplate.clone();
premiumInvoice.currency = "EUR";
premiumInvoice.includeTaxDetails = true;
```

- The new object starts from a known template instead of rebuilding every field from zero.

Avoid:

- using prototype when a normal constructor or plain object creation is already simple and clear

## Practical Checks

- Is creation complex enough to need a pattern at all?
- Am I making the code clearer, or just adding another layer?
- Would a plain constructor or function be simpler?
