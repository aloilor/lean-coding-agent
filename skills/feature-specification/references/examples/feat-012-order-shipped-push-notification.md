# Feature Specification — Order Shipped Push Notification

## Feature

- **ID:** FEAT-012
- **Name:** Order Shipped Push Notification
- **Version:** 1.0
- **Status:** Draft

## Objective

Notify customers on their mobile device when one of their orders ships, so they know it is on its way without opening the app.

## User Stories

**US-1**
As a customer, I want a push notification when my order ships so that I know when to expect it.

**US-2**
As a customer, I want to open the order directly from the notification so that I can see the tracking details.

## Scope

The feature includes:

- sending a push notification to the iOS and Android apps when an order's status changes to Shipped;
- opening the order detail screen when the notification is tapped;
- respecting the existing Order updates notification preference.

## Out of Scope

The following are not included in this feature:

- notifications for any other order status (Confirmed, Out for delivery, Delivered, Cancelled);
- email or SMS notifications;
- notifications in the web application;
- a new notification preferences screen;
- localization beyond the languages the app already supports.

## Functional Requirements

**FR-1 — Trigger**
When an order's status changes to Shipped, the system shall send one push notification to every device on which the order's customer is signed in to the mobile app.

**FR-2 — Content**
The notification shall have the title "Your order has shipped" and the body "Order {orderNumber} is on its way.", in the language selected in the app.

Example: "Order #10482 is on its way."

**FR-3 — Deep link**
Tapping the notification shall open the order detail screen for that order. If the customer is signed out, the app shall open the Sign In screen and show the order detail screen after sign-in.

**FR-4 — Preference**
No notification shall be sent when the customer has turned off Order updates in the app's notification settings.

**FR-5 — Single notification per shipment**
If an order changes to Shipped more than once (for example, after a status correction), the customer shall receive at most one notification for that order.

**FR-6 — Split shipments**
When an order ships in multiple packages, a notification shall be sent only for the first package that ships.

## Acceptance Criteria

**AC-1 — Notification sent**

- **Given** a customer signed in on an Android phone with Order updates turned on
- **When** order #10482 changes to Shipped
- **Then** the phone receives "Your order has shipped — Order #10482 is on its way."

**AC-2 — Opens the order**

- **Given** a customer received the shipped notification for order #10482
- **When** the customer taps the notification
- **Then** the app opens the order detail screen for order #10482

**AC-3 — Preference respected**

- **Given** a customer has turned off Order updates
- **When** one of their orders changes to Shipped
- **Then** no push notification is sent

**AC-4 — Multiple devices**

- **Given** a customer signed in on an iPhone and an iPad
- **When** their order changes to Shipped
- **Then** both devices receive the notification

**AC-5 — No duplicate**

- **Given** a customer already received the shipped notification for an order
- **When** that order's status is changed to Processing and back to Shipped
- **Then** no second notification is sent

## Open Questions

**OQ-1 — Should the notification include the carrier name (e.g. "shipped with DHL")?**
Recommended: no, because the carrier is not always known when the status changes and the order detail screen already shows tracking. Affects: FR-2.

**OQ-2 — For split shipments, should the customer be notified for every package?**
Recommended: only for the first package, to avoid repeated notifications for one order; the order detail screen lists every package. Affects: FR-6.

All open questions must be resolved before the feature is considered approved for development.

## Approval

By approving this specification, the client confirms that the scope, expected behavior, and acceptance criteria described above represent the agreed requirements for FEAT-012 — Order Shipped Push Notification.

- **Client representative:** ______________________
- **Date:** ______________________
- **Approved version:** ______________________
- **Signature / Approval reference:** ______________________
