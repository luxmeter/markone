# JUnit5

Ancestor of JUnit4 composed of three sub-projects: `JUnit 5 = JUnit Platform + JUnit Jupiter + JUnit Vintage`.

Goal is to build a extendible testing platform for the JVM regardless of the language and improve IDE support.

* JUnit Platform
	* Foundation for launching testing frameworks on the JVM
	* Defines TestEngine API for developing testing frameworks
	* Provides ConsoleLauncher to run any TestEngine on the platform from the console
	* Provides plugins / extensions for several build tools (e.g. Maven Surefire Provider)

* JUnit Jupiter
	* Combination of new programming and extension model to write tests and extensions in JUnit5
	* Provides a TestEngine to run JUnit5 tests

* JUnit Vintage
	* Provides TestEngines to run JUnit3 and JUnit4 tests

## Dependencies

Following dependencies have been added to the AclService:

```xml
<!-- API to write JUnit5 tests and extensions -->
<dependency>
	<groupId>org.junit.jupiter</groupId>
	<artifactId>junit-jupiter-api</artifactId>
	<version>5.2.0</version>
</dependency>
<!-- API to write parameterised tests -->
<dependency>
	<groupId>org.junit.jupiter</groupId>
	<artifactId>junit-jupiter-params</artifactId>
	<version>5.2.0</version>
</dependency>
<!-- Provides support classes to migrate Junit4 test to Junit5, i.e. @EnableRuleMigrationSupport -->
<dependency>
	<groupId>org.junit.jupiter</groupId>
	<artifactId>junit-jupiter-migrationsupport</artifactId>
	<version>5.2.0</version>
</dependency>
<!-- Allows to run JUnit3/4 tests in new Junit5 platform-->
<dependency>
	<groupId>org.junit.vintage</groupId>
	<artifactId>junit-vintage-engine</artifactId>
	<version>5.2.0</version>
</dependency>
```

Additionally, these dependencies have been added to the Maven Surefire Plugin to add JUnit5 test provider:
```xml
<dependency>
	<groupId>org.junit.platform</groupId>
	<artifactId>junit-platform-surefire-provider</artifactId>
	<version>1.2.0</version>
</dependency>
<!-- Allows execution of Junit5 tests, only required at runtime (built-in in IntelliJ) -->
<dependency>
	<groupId>org.junit.jupiter</groupId>
	<artifactId>junit-jupiter-engine</artifactId>
	<version>5.2.0</version>
</dependency>
```


## Writing Tests

All core annotations are located in the `org.junit.jupiter.api` package in the `junit-jupiter-api` module.

Tests still look like JUnit4 tests but might have other annotations with different behaviour.

```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class FirstJUnit5Tests {
    @Test
    void myFirstTest() {
        assertEquals(2, 1 + 1);
    }
}
```

Most relevant annotations:

Annotation           | Description
---                  | ---
`@Test`              | Denotes that a method is a test method. Unlike JUnit 4’s @Test annotation, this annotation does not declare any attributes, since test extensions in JUnit Jupiter operate based on their own dedicated annotations. Such methods are inherited unless they are overridden.
`@ParameterizedTest` | Denotes that a method is a parameterized test. Such methods are inherited unless they are overridden.
`@RepeatedTest`      | Denotes that a method is a test template for a repeated test. Such methods are inherited unless they are overridden.
`@DisplayName`       | Declares a custom display name for the test class or test method. Such annotations are not inherited. Supports also Emojis 😱
`@ExtendWith`        | Used to register custom extensions. Such annotations are inherited.
`@Tag`               | Used to declare tags for filtering tests, either at the class or method level; analogous to test groups in TestNG or Categories in JUnit 4. Such annotations are inherited at the class level but not at the method level.
`@BeforeEach`        | Analogous to JUnit 4’s `@Before.` Such methods are inherited unless they are overridden.
`@BeforeAll`         | Analogous to JUnit 4’s `@BeforeClass`. Such methods are inherited (unless they are hidden or overridden).
`@Disabled`          | Used to disable a test class or test method; analogous to JUnit 4’s @Ignore. Such annotations are not inherited.



### Assertions & Assumptions

Assertions API have been updated as well, e.g. there exists now several assertions with support for Stream expressions.

```java
    @Test
    void dependentAssertions() {
        // Within a code block, if an assertion fails the
        // subsequent code in the same block will be skipped.
        assertAll("properties",
            () -> {
                String firstName = person.getFirstName();
                assertNotNull(firstName);

                // Executed only if the previous assertion is valid.
                assertAll("first name",
                    () -> assertTrue(firstName.startsWith("J")),
                    () -> assertTrue(firstName.endsWith("n"))
                );
            },
            () -> {
                // Grouped assertion, so processed independently
                // of results of first name assertions.
                String lastName = person.getLastName();
                assertNotNull(lastName);

                // Executed only if the previous assertion is valid.
                assertAll("last name",
                    () -> assertTrue(lastName.startsWith("D")),
                    () -> assertTrue(lastName.endsWith("e"))
                );
            }
        );
    }

    @Test
    void timeoutNotExceededWithMethod() {
        // The following assertion invokes a method reference and returns an object.
        String actualGreeting = assertTimeout(ofMinutes(2), AssertionsDemo::greeting);
        assertEquals("Hello, World!", actualGreeting);
    }

    @Test
    void testInAllEnvironments() {
        assumingThat("CI".equals(System.getenv("ENV")),
            () -> {
                // perform these assertions only on the CI server
                assertEquals(2, 2);
            });

        // perform these assertions in all environments
        assertEquals("a string", "a string");
    }
	// ...
}
```

### Parameterised Tests

Writing parameterised tests in JUnit4 was cumbersome.
In JUnit5 the API was revised and appear similar to the JUnit4 Parameterise Plugin.
In contrast to the plugin, dynamically created tests can be re-run, e.g. the user can select all failing tests
of a parameterised test case to be re-execute.

```java
@ParameterizedTest
@MethodSource("stringIntAndListProvider")
void testWithMultiArgMethodSource(String str, int num, List<String> list) {
    assertEquals(3, str.length());
    assertTrue(num >=1 && num <=2);
    assertEquals(2, list.size());
}

static Stream<Arguments> stringIntAndListProvider() {
    return Stream.of(
        Arguments.of("foo", 1, Arrays.asList("a", "b")),
        Arguments.of("bar", 2, Arrays.asList("x", "y"))
    );
}
```

Other [source provider](https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests-consuming-arguments):
* `@ValueSource`
* `@EnumSource`
* `@CsvSource`
* `@CsvFileSource`

JUnit5 also allows the user to define `ArgumentConverter` so that the method arguments can consists of complex types.
There are already several implicit conversions defined that are used when importing from a CSV file.

In case a test method accepts too many arguments, a custom `Aggregator` could be used:

```java
@ParameterizedTest
@CsvSource({
    "Jane, Doe, F, 1990-05-20",
    "John, Doe, M, 1990-10-22"
})

void testWithCustomAggregatorAnnotation(@CsvToPerson Person person) {
    // perform assertions against person
}

public class PersonAggregator implements ArgumentsAggregator {
    @Override
    public Person aggregateArguments(ArgumentsAccessor arguments, ParameterContext context) {
        return new Person(arguments.getString(0),
                          arguments.getString(1),
                          arguments.get(2, Gender.class),
                          arguments.get(3, LocalDate.class));
    }
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.PARAMETER)
@AggregateWith(PersonAggregator.class)
public @interface CsvToPerson {
}
```

### Features worth mentioning

* [Test Interfaces and Default Methods](https://junit.org/junit5/docs/current/user-guide/#writing-tests-test-interfaces-and-default-methods)
* [Conditional Test Execution With Javascript support](https://junit.org/junit5/docs/current/user-guide/#writing-tests-conditional-execution)
* [Tagging and Filtering](https://junit.org/junit5/docs/current/user-guide/#writing-tests-tagging-and-filtering)
* [Nested Tests](https://junit.org/junit5/docs/current/user-guide/#writing-tests-nested)

## Extension Model

`@Rules` does not exist anymore in the JUnit5 Platform. Instead, Extensions are written that are inheritable.
Examples are MockitoExtension and the SpringExtension.

### Register Declaratively

Developers can register one or more extensions declaratively by annotating a test interface, test class, test method, or custom composed annotation with @ExtendWith(…​) and supplying class references for the extensions to register.

```java
@ExtendWith(TimingExtension.class)
@Test
void timeit() {
    // ...
}
// INFO: Method [timeit] took 24 ms.
```

### Register Programmatically

It is also possible to register an extension programmatically on an instance field or class field.

```java
class WebServerDemo {

    @RegisterExtension
    static WebServerExtension server = WebServerExtension.builder()
        .enableSecurity(false)
        .build();

    @Test
    void getProductList() {
        WebClient webClient = new WebClient();
        String serverUrl = server.getServerUrl();
        // Use WebClient to connect to web server using serverUrl and verify response
        assertEquals(200, webClient.get(serverUrl + "/products").getResponseStatus());
    }
}
```

### Writing Extensions

The user can define an extension by inheriting from one of the base classes, e.g. `BeforeEachCallback`.

## Migrating to JUnit5

Instead of rewriting all the tests, you can simply use the `vintage` module to run JUnit4 tests in the new JUnit5 platform.
If you want to migrate, you need to reimport the assertions and assumptions and rewrite `@Rules`.
The support for almost all `@Rules` have been dropped except for:

* `org.junit.rules.ExternalResource` (incl. `org.junit.rules.TemporaryFolder`)
* `org.junit.rules.Verifier` (incl.	`org.junit.rules.ErrorCollector`)
* `org.junit.rules.ExpectedException`

To enable the support you have to add the `@EnableRuleMigrationSupport` to the test class.

Notice that `@ClassRules` are not taken into account.

