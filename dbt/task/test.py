
import os, sys
import psycopg2
import yaml

from dbt.compilation import Compiler
from dbt.templates import TestCreateTemplate
from dbt.runner import Runner
from dbt.schema_tester import SchemaTester

class TestTask:
    """
    Testing:
        1) Create tmp views w/ 0 rows to ensure all tables, schemas, and SQL statements are valid
        2) Read schema files and validate that constraints are satisfied
           a) not null
           b) uniquenss
           c) referential integrity
           d) accepted value
    """
    def __init__(self, args, project):
        self.args = args
        self.project = project

    def compile(self):
        compiler = Compiler(self.project, TestCreateTemplate)
        compiler.initialize()
        compiler.compile()

        return compiler

    def run_and_catch_errors(self, func, onFinally=None):
        executed_models = []
        passed = 0

        errored = False
        try:
            for (model, test_passed) in func():
                executed_models.append(model)
                if test_passed:
                    passed += 1
        except psycopg2.ProgrammingError as e:
            errored = True
            print("")
            print("Error encountered while trying to execute tests")
            print("Model: {}".format(e.model))
            print(str(e))
        finally:
            if onFinally:
                onFinally(executed_models)

        if errored:
            print("Exiting.")
            sys.exit(1)
        print("")

        num_passed = len(executed_models)
        print("{passed}/{num_executed} tests passed!".format(passed=passed, num_executed=num_passed))
        print("")

    def run_test_creates(self):
        runner = Runner(self.project, self.project['target-path'], TestCreateTemplate.label)
        self.run_and_catch_errors(runner.run, runner.drop_models)

    def run_validations(self):
        print("Validating schemas")
        schema_tester = SchemaTester(self.project)
        self.run_and_catch_errors(schema_tester.test)

    def run(self):
        compiler = self.compile()

        if self.args.skip_test_creates:
            print("Skipping test creates (--skip-test-creates provided)")
        else:
            self.run_test_creates()

        if self.args.validate:
            self.run_validations()
        else:
            print("Skipping validations (--validate not provided)")

        print("Done!")
