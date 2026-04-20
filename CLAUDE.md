# Bloomerang Mobile App — QE Context

## App Structure

Four tabs: Home, Tasks, Constituent, and More.

**Home Tab**
- Two views: main home screen and activity feed (accessible from home)
- Main home screen shows:
  - **Recent transactions**: the activity feed (most recent 50 across all constituents); tapping a transaction opens a detail view with a link at the top that navigates to the constituent's timeline; donation can be edited here or user can navigate to the constituent timeline
  - **First-time donors (Donor Calls)**: constituents with a phone number who make their first donation; data is sent to the CRM and the API signals the app to update; shows the constituent's profile image and donation; can be tapped to open a detail view with three options:
    - Call Constituent: initiates a phone call
    - New Task: opens a new task creation screen
    - Remove from List: removes the constituent from the widget
    - Any action taken removes the constituent from the Donor Calls widget
    - If no action is taken, the constituent remains in the widget indefinitely — it does not clear on logout or app restart
  - **Campaigns**: custom named values created in the CRM; each campaign shows a progress bar of donation amount progress toward the campaign's goal amount
- Activity feed lists the most recent 50 transactions across all constituents; only donations appear here; no sorting or filtering available — always most recent first; order updates on next load or manual pull-to-refresh, not in real time
- Donations can be opened and edited from the activity feed
- If a donation is a processed transaction, the amount cannot be edited — all other fields can
- FAB is visible on both the main home screen and the activity feed

**Tasks Tab**
- Lists tasks with or without an assigned constituent
- Only shows tasks assigned to the currently logged-in user; tasks assigned to other users do not appear; if a task is reassigned to another user it disappears from the task tab immediately
- A "+" button in the task list banner allows creating a new task directly from the task tab
- Completed tasks are removed from the task tab and can only be viewed from the constituent timeline
- When no tasks are assigned, the task tab displays a message indicating no tasks are currently assigned
- Tasks without an assigned constituent do not require a purpose field
- Tasks with an assigned constituent require a purpose field
- Tasks created on a constituent timeline also appear here
- Tasks are sorted by: overdue (red font) → due today → due later

**Constituent Tab**
- Constituent search and browsing (by name, not real-time — user must tap Search)
- FAB is visible here (create constituent, create timeline entry, quick donation)
- Shows recent constituents (up to 50) under a header, followed by favorited constituents (up to 50); a constituent can appear in both sections simultaneously

**Favoriting Constituents:**
- A constituent can be favorited from their profile page by tapping a star icon
- When favorited, the star fills gold and a gold star appears on their constituent profile image, with a success toast
- Favorites are unlimited — no cap on the number of favorited constituents; sorted by most recently favorited
- Note: both the recent constituents list and the search results list are capped at 50 — the 50 cap does not apply to favorites

**More Tab**
- About the app (app version)
- Payment settings: select a default processor, connect a card swiper or internal card reader
- Link to device settings
- Log out

**Floating Action Button (FAB)**
- Visible on: Home tab (main screen and activity feed) and Constituent tab only — not on Tasks, More tabs, or constituent profile pages
- Options: create a constituent, create a timeline entry (donation, interaction, task, or note), initiate a Quick Donation
- When creating a timeline entry from the FAB: a modal appears first with the 4 entry types to choose from, then the constituent picker is shown to select a constituent (name only, tap Search, 50 result cap); the app then navigates to the create entry page on that constituent's timeline
- All four entry types (donation, interaction, task, note) are available when creating from the FAB

---

## Constituent Profile Page

The constituent page has two tabs:

**Timeline Tab (default)**
- Header: profile picture (changeable/deletable; blank avatar shown when no photo is set), favorite button, engagement bar (a bar graph showing giving and involvement history back to when the constituent record was created), total donation amount, YTD donation amount, and latest donation amount
- Giving summary graph showing raised and revenue values over time, back to when the constituent record was created
- A link to add a timeline entry appears at the top of the timeline, just below the constituent banner; tapping it shows a modal with the 4 entry types (same as FAB) but with no constituent picker — the entry is created directly on the current constituent's timeline
- Full timeline loads in its entirety — no pagination or lazy loading
- All entry types (donations, interactions, tasks, notes) in one combined list, sorted newest to oldest — no filtering by type
- When a constituent has no timeline entries, the timeline tab shows an empty state with no message
- Entries can be deleted by opening the entry and tapping the delete option at the bottom; a confirmation prompt is shown before deletion completes; processed transactions (credit card, EFT) cannot be deleted
- Deleting an entry removes everything associated with it, including attachments — attachments are directly tied to their entry
- Timeline order is determined by entry date; entries can only be reordered by editing their date
- Pull-to-refresh is the only gesture supported in the app; no swipe-to-delete or other swipe gestures
- Each entry type is visually distinguished by its own icon
- All entries display: entry icon and date
- Donation entries also show: amount, donation type label, fund, and video acknowledgement widget
  - Donation type labels: one-time shows amount only; pledge setup shows amount + "Pledge"; pledge payment shows amount + "Pledge Payment"; recurring donation setup shows amount + "Recurring Donation"; recurring donation payment shows amount + "Recurring Donation Payment"; refunds show amount + "Refund"
  - The following entry types appear on the mobile timeline but cannot be opened, created, or edited — tapping them shows a toast that they are not yet available in the mobile app and can be managed in the CRM: initial pledge setup, initial recurring donation setup, memberships, membership payments
  - VA widget states: lock icon (no license) | "+ Video" button (licensed, not yet sent) | checkmark with grayed-out button (VA sent)
- Interaction entries also show: subject, purpose, channel
- Task entries also show: subject, purpose, channel
- Note entries also show: "Note" label with a preview of the note text

**Profile Tab**
- Edit basic profile details (all constituent profile fields can be edited from the app; syncs to CRM via API; profile picture changes are reflected in the CRM)
- Add to or create a household
- Create a relationship with another constituent (standard relationship types exist; custom types can be created in the CRM — relationships are display only with no other dependencies; relationship shows on both constituent records)
- View groups the constituent belongs to (groups are established in the CRM; the app displays what the API returns — read only, cannot be edited or altered)
- Display and edit contact information: phone numbers, email addresses, mailing addresses, social media links (Facebook, Twitter, LinkedIn, and website URL — all are hyperlinks that open the respective app if installed, or a webpage if not)
  - Any number of phone numbers, emails, and addresses can be added
  - The first entry added becomes the primary by default
  - Additional entries can be marked as primary via a checkbox; the new primary moves to the top of that section
  - Primary phone, email, and address are used for household contact info, Quick Contact, and email options
- Quick Contact button: initiates a call, text, or email depending on available and unrestricted contact options; when the user returns to the app after initiating a call, text, or email, they are prompted to create an interaction — if they accept, a new interaction screen opens with the channel field pre-populated (call, text, or email); no other fields are pre-populated

---

## Constituents

**Types:**
- Individual (requires first name and last name)
- Organization (requires organization name only; uses organization name instead of first/last name fields throughout the app)

**Constituent management:**
- Constituent deletion and merging are CRM only — cannot be done from the app
- Required fields are enforced when editing an existing constituent — they cannot be cleared and saved
- Only individual constituents can be added to households — organizations cannot
- A constituent can only belong to one household at a time; they must be removed from their current household before being added to another

**Households:**
- A household is its own record type — not just a grouping
- Constituents can be added to or create a household from the constituent timeline; when creating a new household, the constituent who initiates creation automatically becomes the head of household and first member
- Households compile all entry types (transactions, interactions, notes, tasks) from all members — the household timeline consists of each individual member's complete personal timeline entries
- Household timeline is sorted newest to oldest regardless of which member the entry belongs to
- Transactions can only be made for individual constituents, not directly for a household
- Entries viewed from the household timeline navigate to the specific constituent record where they can be edited
- If a constituent is removed from a household, their entries are removed from the household timeline
- The head of household's contact information becomes the default contact information for the household; changes to head of household update contact information immediately
- Head of household is set when creating a household or from the household profile

**Household profile page:**
- Same two-tab layout as a constituent (timeline + profile)
- Timeline tab displays all member entries compiled together
- Profile tab: displays all household members; members can be removed, navigated to their constituent record, or made head of household
- Only the household name can be edited on the household record

**Constituent Search:**
- Available in Quick Donation, task creation, and the constituent tab
- Search is by name only
- Not real-time — user must type a value and tap Search to see results
- No results state displays "no results"

**Recent constituents:**
- Up to 50 recent constituents shown on the Constituent tab
- "Recent" is determined by last viewed
- Organization constituent records can appear in recents and favorites alongside individual constituents
- Organizations and household records appear in constituent search results alongside individual constituents; search is by name only for all types; household records display the household name in search results and can be tapped to navigate directly to the household record
- Search results are capped at 50 — if more than 50 matches exist, only 50 are shown with no indication that results were truncated

---

## Timeline Entries

All entries are created via the FAB or from a constituent's timeline page. All entries show on the constituent timeline. If a constituent is a member of a household, entries also appear on the household timeline. Donations (whether created via Quick Donation or from the constituent timeline) also appear on the activity feed.

**Editing:**
- All entry types can be edited from the constituent timeline
- Only donations appear on the activity feed; donations can also be edited there; the editing experience is identical whether accessed from the activity feed or the constituent timeline
- All entry types can be deleted; processed transactions (CC or EFT) cannot be deleted
- If a donation is a processed transaction, the amount field cannot be edited

### Donation

**Types:**
- One-time
- Recurring donation setup — created in CRM; appears on timeline but cannot be opened or edited from the app
- Recurring donation payment — individual payments made against a recurring schedule; can be added from the app (schedule must be set up in CRM first)
- Pledge setup — created in CRM; appears on timeline but cannot be opened or edited from the app
- Pledge payment — individual payments made against a pledge; can be added from the app (pledge must be set up in CRM first)

**Donation type selection:**
- If a constituent has a recurring payment and/or pledge set up in the CRM, initiating a donation shows a selection screen first — one-time, recurring payment, or pledge; only one can be selected

**Pledge payment fields:**
- Shows next payment due date and whether the constituent is in arrears
- Fund: pre-populated, cannot be edited
- Date: pre-populated, required
- Amount: required
- Method: required

**Recurring payment fields:**
- Shows due date and whether the payment is overdue
- Payment type toggle: Scheduled (advances the due date based on the recurrence interval set in the CRM — weekly, monthly, quarterly, etc.) or Extra (does not impact due date — due date remains unchanged)
- Date: pre-populated, required
- Amount: pre-populated, cannot be edited
- Method: required
- Fund: pre-populated, required, can be edited

**Refunds:**
- Refunded transactions appear wherever transactions are displayed — activity feed, constituent timeline, and household timeline
- Refunds look the same as regular transactions in the list; tapping one displays a toast indicating it can only be viewed in the CRM
- Refunds can only be initiated from the CRM

**Donation detail view:**
- Displays all values that were entered on the create/edit page
- No additional metadata (e.g., no confirmation number or processor status beyond what was entered)
- On processed donations (CC or EFT), the payment method cannot be changed when editing; all other unprocessed methods can be changed freely, including switching to a processed method

**Automatic receipting:**
- If the CRM has automatic receipting enabled AND the constituent has an email address on file, creating a donation automatically:
  - Sends an email receipt to the constituent
  - Creates an interaction on the constituent's timeline with channel set to "Receipt"; this interaction is fully editable by the user

**Required fields:**
- Date (auto-populated)
- Amount
- Method
- Fund (dropdown, managed in CRM; only one fund per donation)

**Available methods and fields:**
- Cash: no extra fields
- Check: check number and check date (both optional)
- Credit card: processor, input type (options: manual entry, card swiper, tap to pay)
- EFT: processor, account type (checking or savings), routing number, account number — error is thrown if routing or account number is invalid
- Credit card (manual entry): error messages are shown if card details are incorrect
- Payment processing failures (e.g., card declined): error toast displayed with a message specific to the failure; the app handles some failures gracefully with multiple error states
- In-kind: type (dropdown: Goods / Services), fair market value, and description (all optional); in-kind donations are never processed — they are recorded only
- Apple Pay: processor — functions the same as tap to pay; tap screen appears on the user's device; both Apple Pay and Google Pay are available on both iOS and Android — the user selects whichever matches the donor's device
- Google Pay: processor — functions the same as tap to pay; tap screen appears on the user's device
- PayPal: no extra fields
- Venmo: no extra fields
- Saved payments: appears as a method option if the constituent has a previously saved credit card or EFT on file; displays the last 4 digits of the saved card/account; pre-populates saved payment details; saved payments can only be selected/processed in the app — editing or deleting is CRM only
- Processed credit card and EFT transactions display the last 4 digits of the card/account on the transaction detail page

### Interaction

Interactions are always tied to a constituent — they cannot be created without one.

**Required fields:**
- Date (auto-populated)
- Subject
- Purpose (dropdown, managed in CRM; values are specific to interactions)
- Channel (dropdown, managed in CRM; separate list from task channel values; all managed in CRM)

### Task

**Required fields:**
- Assignee (auto-populated to the logged-in user; can be changed or reassigned to any user in the org after creation)
- Date (auto-populated; serves as the task due date)
- Subject
- Purpose (dropdown, managed in CRM; separate list from interaction purpose values; required only if a constituent is assigned; not required on task tab without a constituent)
- Channel (dropdown, managed in CRM; separate list from interaction channel values)

**Task detail view actions:**
- Once a constituent is assigned to a task and saved, the constituent cannot be removed — the task remains tied to that constituent
- A task can be reassigned to a different user after creation
- Complete Task: removes the task from the task tab immediately; on the constituent timeline the task remains visible sorted by its completed date; the task detail page shows a read-only Status field set to Complete
- Complete Task and Make Follow-up: closes the current task and opens a new task creation screen
- Create Interaction: opens a new interaction creation screen from within the task detail view; the constituent is automatically associated; the interaction is a separate entity with no reference back to the originating task

### Note

**Required fields:**
- Date (auto-populated, but can be edited to any date)
- Notes (text body only — no subject or title field)

**All entry types** (donations, interactions, tasks, notes) include an optional free-text notes field in addition to their required fields.

---

## Payment Processors

### Bloomerang Payments (Stripe Express)
- Supported methods: credit card (manual entry, card swiper, tap to pay), EFT, Apple Pay, Google Pay
- Quick Donation: supported
- Legacy processor — existing customers only; will eventually be migrated to 1-Pay

### Bloomerang Payments (1-Pay / Stripe Custom)
- Supported methods: credit card (manual entry, card swiper, tap to pay), EFT, Apple Pay, Google Pay
- Quick Donation: supported
- New customers only for now; will eventually replace Stripe Express for all Bloomerang Payments customers

**Note:** An org can only ever have one Bloomerang Payments processor — either Stripe Express or 1-Pay, never both.

### Stripe
- Supported methods: credit card (manual entry, card swiper), EFT
- Quick Donation: not supported — standard timeline entry only

### Bluepay (Legacy)
- Supported methods: credit card (manual entry only), EFT, Do Not Process
- Quick Donation: not supported — standard timeline entry only

### Authorize.net (Legacy)
- Supported methods: credit card (manual entry only), EFT, Do Not Process
- Quick Donation: not supported — standard timeline entry only

### Do Not Process
- Available for all processors
- Records the transaction but does not actually process a payment
- Displays on the activity feed like a standard transaction; treated similarly to a cash donation

### Processor Selection and Defaults
- Processor is a dropdown field on donation creation and in payment settings (More tab)
- Default behavior:
  - If the org has only one processor, it is always selected automatically
  - If the user has previously selected a processor, that becomes their default
  - If the org has Bloomerang Payments, it defaults to Bloomerang Payments **unless** the user has previously selected a different processor
  - If the org has multiple processors and the user has never selected one, they must choose manually
- Changing the processor during donation creation updates the user's default going forward
- If a user has never selected a processor and the org has multiple, the processor field in Quick Donation and donation creation is unpopulated and must be selected before proceeding

### Tap to Pay and Card Swiper
- Tap to Pay (T2P): available on Bloomerang Payments only; auto-connects on login if Bloomerang Payments is the default processor; can also be manually reconnected via a button on the Payment Settings page; tap screen appears on the user's device during payment
- Card swiper: available on Stripe and both Bloomerang Payments processors; supports any Stripe card reader (most commonly the M2 Chipper); can only be connected via a button on the Payment Settings page (More tab)
- Connection failures show an error toast
- If location or Bluetooth permissions are denied, the app prompts the user to enable them in device settings
- If Bluetooth drops during a Tap to Pay transaction, an error toast is displayed and the app attempts to reconnect

### Method Summary

| Method | Bloomerang Payments | 1-Pay | Stripe | Bluepay | Authorize.net |
|---|---|---|---|---|---|
| CC - Manual entry | ✓ | ✓ | ✓ | ✓ | ✓ |
| CC - Card swiper | ✓ | ✓ | ✓ | ✗ | ✗ |
| CC - Tap to pay | ✓ | ✓ | ✗ | ✗ | ✗ |
| EFT | ✓ | ✓ | ✓ | ✓ | ✓ |
| Apple Pay | ✓ | ✓ | ✗ | ✗ | ✗ |
| Google Pay | ✓ | ✓ | ✗ | ✗ | ✗ |
| Do Not Process | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## Quick Donation Flow

- Accessible via FAB
- Only available when the org's processor is Bloomerang Payments (Stripe Express) or Bloomerang Payments (1-Pay) — Stripe, Bluepay, and Authorize.net orgs do not see the Quick Donation option
- Supported methods: credit card, EFT, Apple Pay, Google Pay

**Flow:**
1. Donation details screen: amount (editable; also shown and editable on screen 2), payment method, input type, fund, and processor
2. Constituent screen: amount (editable), constituent picker to search for and select an existing constituent, or fields below to create a new one (first name, last name, phone, email)
   - Amount can remain 0 throughout the entire flow; only when "Donate Now" is tapped does validation trigger — amount field turns red and donation cannot be submitted until a value is entered
   - First name and last name are required for new constituents; phone and email are optional
   - If an existing constituent is selected, the new constituent fields disappear and the constituent's info is displayed
   - If search returns no results, the new constituent fields remain visible and the user can proceed to create a new constituent
   - A new constituent created here results in a standard constituent record in the CRM
3. User taps "Donate Now" to complete
- If the user cancels at any point during the Quick Donation flow, nothing is saved — no constituent or transaction is created
- If a user is creating any entry (donation, interaction, task, note) and cancels, nothing is saved; the one exception is if the user navigates to another tab without explicitly canceling and then returns — in that case, data may be preserved (applies to all tabs, not just the constituent tab)

**vs. timeline donation:**
- Timeline donation begins from a constituent record — the constituent is already known, so it goes directly to the donation creation form
- Quick Donation begins with donation details first, then constituent selection/creation
- QD flow is the same regardless of payment method — EFT, CC, and all other methods follow the same two-screen flow
- Quick Donation always creates a one-time donation — recurring payment and pledge payment types are not available in QD, even if the selected constituent has a recurring schedule or pledge set up

---

## Attachments

- All timeline entry types (donations, interactions, tasks, notes) support attachments
- Attachment types: image or URL
- Image attachments sync to the CRM
- When an attachment is present, a paperclip icon is shown on the timeline entry

---

## Push Notifications

- Overdue task notifications are currently supported — sent even when the app is closed
- One notification is sent for all overdue tasks (not one per task) at 9AM EST
- Tapping an overdue task notification currently does not navigate anywhere in the app
- Donation notifications are in development (not yet live)

---

## Platform

- App name: Bloomerang CRM (App Store and Google Play)
- iOS and Android
- Built with .NET MAUI (cross-platform)
- iOS and Android builds behave the same — no known platform-specific differences
- English only — no localization support
- No forced updates — outdated versions continue to work; Pendo is used ad hoc (not always active) and has been used in the past to prompt updates for major feature releases
- QE tests on the latest internal test build distributed via Firebase; production testing uses TestFlight (iOS); production releases go through the App Store and Google Play

## Accessibility

- The app supports device visual accessibility settings, including enlarged/dynamic font sizes
- UI designs must account for enlarged font — text truncation, layout overflow, and button sizing should be tested with large font enabled

## Offline Behavior

- No offline functionality; the app requires a network connection
- When not connected, an error toast is displayed

## Data Refresh

- All pages refresh when initially loaded or on manual pull-to-refresh
- No automatic background refresh while a page is being viewed

## Authentication

- Login screen supports standard username/password input
- Biometric authentication (Face ID / fingerprint) triggers automatically on app open if configured on the device — there is no explicit biometric login button; if biometrics are not set up, the user must log in manually
- No SSO, no org URL entry, no forgot password from the app
- No onboarding, walkthrough, or setup screens on first login
- Users are tied to a single Bloomerang org instance
- Session timeout exists but is quite long (exact duration unknown)
- Permission changes require a logout and login to take full effect
- Timeline additions and edits made in the CRM are reflected when the user navigates to that page or manually refreshes

## Device Permissions

The app requests the following device permissions:
- Camera and photo library (profile photos, image attachments, video acknowledgements — user can choose camera or library for images)
- Microphone (video acknowledgements)
- Bluetooth (card swiper, tap to pay)
- Location (required for tap to pay)
- Notifications — if denied, the user must re-enable through device settings; the app does not prompt to re-enable from within the app

## Permissions

Permissions are configured in the CRM. The following user types exist:

| Role | Transactions | Edit | Home Tab |
|---|---|---|---|
| Admin | All | Yes | Always visible |
| Standard - View and Edit All | All | Yes | Can be disabled |
| Standard - View Only | All | No | Can be disabled |
| Standard - View and Edit Own | Own transactions only (transactions by other users cannot be viewed); activity feed shows only their transactions if home tab is enabled | Own only | Can be disabled |
| Standard - No Access | None (cannot view any transactions) | No | Can be disabled |

- For all standard user types, the home tab can be optionally disabled by an admin in the CRM
- When home tab is disabled, the user does not see it in the app

---

## Video Acknowledgements

- Available on every donation record
- If the org does not have a Video Acknowledgement license, a lock icon is shown; tapping the lock icon displays a popup explaining how to obtain the license
- If licensed, the user can initiate a video acknowledgement from the donation

**Flow:**
1. User initiates video acknowledgement from a donation
2. Recording screen opens — user records a video, then saves or cancels; user can cancel and re-record at this stage
3. If saved, user is taken to a preview screen to review the video; user can cancel and re-record from the preview screen as well
4. After confirming, user reaches an email preview screen with:
   - Subject line (auto-populated, required, editable)
   - Message body (auto-populated, required, editable)
   - Video thumbnail (auto-populated, editable — user can select a different thumbnail image to display in the email)
5. User sends the email via the UGA service
6. A toast displays confirming the video is being processed and the email was sent
7. The donation record reflects that a video acknowledgement was sent
8. An interaction is automatically created silently on the constituent's timeline with channel set to "Video Acknowledgement"
- Only one video acknowledgement can be sent per donation

**Prerequisites to send:**
- Org must have a Video Acknowledgement license (license is per-org, not per-user)
- Constituent must have an email address on file

---

## Custom Fields

- CRM users can create custom field types for timeline entries
- Custom fields can be marked as required
- Required custom fields must be treated as required in the app — a test area worth checking when custom fields are involved in a ticket
