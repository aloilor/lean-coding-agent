# Creational Patterns

## Factory

- A factory creates an object on behalf of the caller.
- Use it when object creation includes choice, setup, or wiring that should not be repeated everywhere.
- The caller should ask for "the thing it needs" and not care which concrete class or setup steps are behind it.

In simple terms:

- `new` is for direct, obvious construction.
- A factory is for "figure out which object to build, then build it correctly."

Good examples:

- `paymentGatewayFactory.create(provider)`
- `notificationSenderFactory.create(channel)`
- `storageClientFactory.create(environment)`
- `reportExporterFactory.create(format)`

More examples:

- `parserFactory.create(fileType)` returns `CsvParser`, `JsonParser`, or `XmlParser`
- `authHandlerFactory.create(strategy)` returns `PasswordAuthHandler`, `GoogleAuthHandler`, or `SamlAuthHandler`
- `cacheFactory.create(environment)` returns an in-memory cache for local development and Redis for production
- `shippingCalculatorFactory.create(region)` returns the pricing rules object for the destination country or market
- `documentRendererFactory.create(outputFormat)` returns a PDF, HTML, or Markdown renderer with the right dependencies already configured

Simple example:

```ts
const gateway = paymentGatewayFactory.create(provider);
```

What the factory is doing for the caller:

- If `provider` is `"stripe"`, it can return `StripeGateway`.
- If `provider` is `"paypal"`, it can return `PaypalGateway`.
- It can also apply setup rules such as API keys, retry settings, or test vs production configuration.
- The caller just asks for a gateway and uses it.

That matters because without the factory, the selection and setup logic often gets copied into multiple places.

Another way to think about it:

- Good: "Give me a payment gateway for this provider."
- Less good: "Let me decide which class to instantiate and how to configure it here again."

Use a factory when:

- one request can lead to different concrete implementations
- object creation needs a few steps, not just one constructor call
- setup depends on environment, format, provider, or feature flags
- you want the creation rules in one place instead of scattered across the codebase

For example:

- A parser factory hides which parser class matches the input file type.
- A cache factory hides whether the app should use a lightweight local cache or a production cache backend.
- An auth handler factory hides the strategy-specific setup needed for each login method.

Avoid:

- Adding a factory for a class that could just be created with `new UserService(...)`.
- Wrapping a single constructor in a factory when there is no selection or setup logic to hide.
- Introducing `somethingFactory.create()` just because "factories are a pattern."

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

More examples:

- one metrics registry that the application initializes once at startup and all modules report into
- one in-memory scheduler registry that tracks jobs for the current running process only
- one application-wide configuration object loaded once during bootstrap and treated as read-only afterward
- one connection pool manager only if the application lifecycle guarantees there should be exactly one shared pool per process

Simple example:

- one shared logger used across the whole application
- one shared config registry loaded once at startup

Concrete examples:

- `AppLogger.getInstance()` returns the single logger configured during application startup
- `FeatureFlagRegistry.getInstance()` returns the one in-memory registry for the running process
- `MetricsRegistry.getInstance()` returns the one collector that all requests publish counters and timings to

- The key idea is not "make it global because it is convenient".
- The key idea is "there should truly be only one shared instance".

Avoid:

- using a singleton just to make access easy from anywhere
- using a singleton for request-specific state, such as the current user or current tenant
- using a singleton when tests need different instances or isolated state between runs

Bad example:

- `CurrentUserContext.getInstance()` as a global mutable object usually causes hidden coupling and test leaks

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
