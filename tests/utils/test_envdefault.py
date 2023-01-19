import argparse
import os
from unittest import TestCase
from unittest import mock

from garminworkouts.utils.envdefault import EnvDefault


class EnvDefaultTestCase(TestCase):
    _ANY_ENV_VAR_NAME = 'TEST_ENV_VAR'

    def test_from_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--test", action=EnvDefault, env_var=EnvDefaultTestCase._ANY_ENV_VAR_NAME, required=True)

        args = parser.parse_args(['--test', 'foo'])
        self.assertEqual(args.test, 'foo')

    @mock.patch.dict(os.environ, {_ANY_ENV_VAR_NAME: "foo"})
    def test_from_envs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--test", action=EnvDefault, env_var=EnvDefaultTestCase._ANY_ENV_VAR_NAME, required=True)

        args = parser.parse_args([])
        self.assertEqual(args.test, 'foo')

    @mock.patch.dict(os.environ, {_ANY_ENV_VAR_NAME: "foo"})
    def test_args_take_precedence_over_envs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--test", action=EnvDefault, env_var=EnvDefaultTestCase._ANY_ENV_VAR_NAME, required=True)

        args = parser.parse_args(['--test', 'bar'])
        self.assertEqual(args.test, 'bar')
