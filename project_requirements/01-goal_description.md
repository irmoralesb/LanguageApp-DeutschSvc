# Description

The German Verbs service helps users learn **German verb conjugations** by tense and person in context.

# Goals

* The user can practice German verbs for learning or improving German grammar and vocabulary.

## Functional Requirements

### Application management

* The service must ship with an initial **catalog of German verbs** (infinitive, definition, and conjugations).
    * An admin user can extend the catalog.
* Supported language list:
    * English
    * German
* Native language
    * This is the language the end user speaks; the list must include Spanish.
    * Catalog: supported languages, including the top five most spoken languages in the world.
* The service will keep information for each user:
    * The user id
    * Native language and learning languages
    * The selected **German verbs** from the catalog
        * The user may add custom verbs where the product allows it.
    * The application will keep a record of:
        * How many times each practice item was answered correctly or incorrectly
        * Feedback: analysis of the detected failure reason, if any

### End user

* The user
    * chooses the target language(s)
    * can select a subset of German verbs from the catalog; this selection is stored per user
    * can choose a specific verb to practice or enable random mode
    * can practice a selected tense and grammatical person

### German verb exercise types

#### Writing — verb conjugation exercise

##### Prerequisites

* Native and target user language. This is required.
* Optional: narrow the situation (e.g. office, street) for more targeted prompts.

##### Exercise

* The service will generate:
    1. A scenario in the native language, with a short description, so the user has context
    2. A prompt in the native language asking the learner to write the correct German verb conjugation for the requested tense and person

##### Answer

* The user writes the correct German conjugated verb form for the requested tense and person.

##### Evaluation

* The system evaluates whether the answer is acceptable (correct tense, person, and spelling).
* It returns feedback (correct/incorrect); if incorrect, it should give a clear corrective example where possible.

## Non-functional requirements

* This Web API is part of the current solution; **`LanguageApp-IdentitySvc`** is the identity service for the portal.
* Use the current Web API project structure and architecture.
    * Improvements may be suggested but require approval first.
* Use SOLID principles.
* Use clean architecture.
* Use current packages when possible.
* The language engine is an LLM (e.g. OpenAI or Anthropic); the application must support switching providers.
* Use Microsoft SQL Server to store required data.
    * Use Alembic for schema migrations.
    * A different or complementary store may be added if needed.
* Each request must authenticate the user and be traceable with a request id.
* Each request should integrate with the Azure Monitor setup already used in the project.
* Use Docker containers.
    * Provide Docker files for the Web API and database where applicable.

## Security requirements

* The Web API grants access to authenticated users.
* Endpoints that perform user or service administration must be restricted to the administrator role defined in the identity service.
* Other endpoints must validate that the user has the **`german-verbs-user`** role (under the **`german-verbs-service`** JWT roles key).
* Log security-relevant activity using Azure services.
