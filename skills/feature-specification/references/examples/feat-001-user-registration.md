# Feature Specification — User Registration with Email Verification

## Feature

- **ID:** FEAT-001
- **Name:** User Registration with Email Verification
- **Version:** 1.1
- **Status:** Proposed

## Objective

Allow new visitors to create an account with an email address and password, and require them to verify that email address before they can sign in, so that every active account is tied to a mailbox its owner controls.

## User Stories

**US-1**
As a new visitor, I want to create an account with my email address and a password so that I can start using the application.

**US-2**
As a new visitor, I want to confirm my email address through a link so that I know my account is set up correctly.

**US-3**
As a registered user who did not receive the verification email, I want to request a new one so that I can complete my registration.

## Scope

The feature includes:

- a public registration form collecting full name, email address, and password;
- validation of the submitted data;
- sending a verification email containing a single-use link;
- verifying the email address when the link is opened;
- resending the verification email on request;
- blocking sign-in for accounts whose email address is not verified.

## Out of Scope

The following are not included in this feature:

- registration or sign-in through third-party identity providers (Google, Apple, Microsoft);
- invitation-based registration by administrators;
- password reset;
- multi-factor authentication;
- changing the email address after registration;
- CAPTCHA or other bot-detection challenges;
- automatic deletion of accounts that are never verified.

## Actors and Permissions

The feature is available to:

- unauthenticated visitors (registration and verification);
- registered users with an unverified email address (resend verification).

Authenticated users with a verified email address shall not be able to access the registration form; they shall be redirected to the dashboard.

## Preconditions

- The visitor is not signed in.
- The application can send transactional email.

## Functional Requirements

**FR-1 — Registration form**
The Sign Up page shall provide a form with the fields Full name, Email, and Password, and a Create account action.

**FR-2 — Full name validation**
Full name shall be required and shall contain between 1 and 100 characters after leading and trailing whitespace is removed.

**FR-3 — Email validation**
Email shall be required, shall be a syntactically valid email address, and shall be compared case-insensitively.

**FR-4 — Password policy**
Password shall contain at least 12 characters and at most 128 characters. No other composition rules shall be enforced.

**FR-5 — Account creation**
When a visitor submits a valid form for an email address that is not already registered, the system shall create an account in the Unverified state.

**FR-6 — Verification email**
When an account is created, the system shall send a verification email to the registered address containing a single-use verification link.

**FR-7 — Uniform confirmation**
After any valid submission, the system shall display the message "Check your inbox to confirm your email address", regardless of whether the email address was already registered.

**FR-8 — Already-registered email**
When a valid form is submitted for an email address that is already registered, the system shall not create a new account and shall send that address an email stating that an account already exists, with a link to the Sign In page.

**FR-9 — Email verification**
When a visitor opens a valid, unexpired verification link, the system shall mark the account as Verified and display the Sign In page with the message "Your email address is confirmed. You can now sign in."

**FR-10 — Unverified sign-in**
When a user with an unverified account signs in with correct credentials, the system shall not start a session and shall display a message offering to resend the verification email.

**FR-11 — Resend verification**
The system shall allow an unverified user to request a new verification email from the Sign In page.

**FR-12 — Duplicate submissions**
Repeated submissions of the registration form for the same email address within 10 seconds shall not create more than one account or send more than one verification email.

## Business Rules

**BR-1**
An email address shall belong to at most one account.

**BR-2**
Verification links shall expire 24 hours after they are issued.

**BR-3**
Issuing a new verification link shall invalidate all previously issued links for that account.

**BR-4**
Responses to registration and resend requests shall not reveal whether an email address is registered.

## Error Handling and Edge Cases

**EC-1 — Invalid form data**
If any field fails validation, the form shall remain populated except for Password, and an error message shall be displayed next to each invalid field.

**EC-2 — Expired link**
If an expired verification link is opened, the system shall display "This link has expired" and offer to send a new verification email.

**EC-3 — Already-used or invalidated link**
If a verification link that has already been used or invalidated is opened, the system shall display "This link is no longer valid" and a link to the Sign In page. The account state shall not change.

**EC-4 — Email delivery failure**
If the verification email cannot be handed to the email provider, the account shall still be created, and the user shall be able to request a resend from the Sign In page.

**EC-5 — Resend rate limit**
No more than 5 verification emails shall be sent to the same address within one hour. Requests beyond the limit shall show the uniform confirmation message without sending an email.

**EC-6 — Email case and whitespace**
` Alice@Example.com ` and `alice@example.com` shall be treated as the same email address.

## Acceptance Criteria

**AC-1 — Successful registration**

- **Given** a visitor on the Sign Up page
- **When** the visitor submits a valid full name, an unregistered email address, and a 12-character password
- **Then** an Unverified account is created
- **And** a verification email is sent to that address
- **And** the message "Check your inbox to confirm your email address" is displayed

**AC-2 — Password too short**

- **Given** a visitor on the Sign Up page
- **When** the visitor submits a password of 11 characters
- **Then** no account is created
- **And** an error is displayed next to the Password field

**AC-3 — Already-registered email does not leak**

- **Given** an account already exists for `alice@example.com`
- **When** a visitor registers with `Alice@Example.com`
- **Then** no new account is created
- **And** the same confirmation message as AC-1 is displayed
- **And** `alice@example.com` receives an "account already exists" email

**AC-4 — Successful verification**

- **Given** an Unverified account with a verification link issued 1 hour ago
- **When** the user opens the link
- **Then** the account becomes Verified
- **And** the Sign In page shows "Your email address is confirmed. You can now sign in."

**AC-5 — Expired link**

- **Given** a verification link issued 25 hours ago
- **When** the user opens the link
- **Then** the account remains Unverified
- **And** the page shows "This link has expired" with an option to send a new email

**AC-6 — Old link after resend**

- **Given** an Unverified user requested a resend after receiving a first verification email
- **When** the user opens the link from the first email
- **Then** the page shows "This link is no longer valid"
- **And** the account remains Unverified

**AC-7 — Unverified sign-in blocked**

- **Given** an Unverified account
- **When** the user signs in with the correct email and password
- **Then** no session is started
- **And** the user is offered to resend the verification email

**AC-8 — Resend rate limit**

- **Given** 5 verification emails were sent to an address in the last hour
- **When** a sixth resend is requested for that address
- **Then** no email is sent
- **And** the uniform confirmation message is displayed

**AC-9 — Double submit**

- **Given** a visitor on the Sign Up page with a valid form
- **When** the visitor triggers Create account twice within 10 seconds
- **Then** exactly one account is created
- **And** exactly one verification email is sent

**AC-10 — Signed-in user redirected**

- **Given** a signed-in user with a verified email address
- **When** the user navigates to the Sign Up page
- **Then** the user is redirected to the dashboard

## UI / UX Reference

- The Sign Up page is reachable from a "Create an account" link on the Sign In page.
- Field order, labels, and error placement shall follow the approved authentication screen designs (Figma: "Auth / Sign Up v3"), which are binding for this feature.
- The verification email uses the existing transactional email layout.

## Non-Functional Requirements

**NFR-1 — Password storage**
Passwords shall be stored only as salted hashes using an algorithm designed for password storage; plaintext passwords shall never be logged, stored, or emailed.

**NFR-2 — Link security**
Verification links shall contain an unguessable token of at least 128 bits of entropy.

**NFR-3 — Performance**
The registration request should complete within 1 second at the 95th percentile, excluding email delivery time.

**NFR-4 — Accessibility**
The Sign Up page shall meet WCAG 2.2 level AA.

**NFR-5 — Audit**
Account creation and email verification events shall be recorded in the existing audit log with timestamp and account identifier.

## Dependencies and Assumptions

- A transactional email provider is already configured and used by the application.
- The existing audit log can accept new event types.
- The Sign In page exists and can display informational messages.
- Unverified accounts are retained indefinitely; cleanup will be specified separately if needed.

## Open Questions

None. All questions raised in version 1.0 (password policy, link expiry, rate limit) were resolved with the client on 2026-09-28 and are reflected in FR-4, BR-2, and EC-5.

All open questions must be resolved before the feature is considered approved for development.

## Approval

By approving this specification, the client confirms that the scope, expected behavior, and acceptance criteria described above represent the agreed requirements for FEAT-001 — User Registration with Email Verification.

- **Client representative:** ______________________
- **Date:** ______________________
- **Approved version:** ______________________
- **Signature / Approval reference:** ______________________
