"""Fast regression checks; real namespace ownership is covered by eturnal.robot."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPAIR = ROOT / 'imageroot/actions/update-module/04repair_state_ownership'
RESTART = ROOT / 'imageroot/update-module.d/20restart'


class UpgradeHooks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.state = self.base / 'state with spaces'
        self.state.mkdir()
        self.log = self.base / 'calls'
        self.env = dict(os.environ, PATH=f'{self.base}:{os.environ["PATH"]}',
                        AGENT_STATE_DIR=str(self.state), CALLS=str(self.log))
        self.mock('podman', 'printf "%s\\n" "$@" >> "$CALLS"\nexit "${PODMAN_RC:-0}"')
        self.mock('systemctl', '''printf "%s\\n" "$@" >> "$CALLS"
case " $* " in *" is-enabled "*) exit "${ENABLED_RC:-0}";; esac
exit "${RESTART_RC:-0}"''')

    def mock(self, name, body):
        path = self.base / name
        path.write_text('#!/bin/bash\n' + body + '\n')
        path.chmod(0o755)

    def run_hook(self, path):
        return subprocess.run([str(path)], env=self.env, capture_output=True)

    def calls(self):
        return self.log.read_text().splitlines() if self.log.exists() else []

    def test_repair_uses_namespace_and_is_repeatable(self):
        config = self.state / 'eturnal.yml'
        config.write_text('secret: keep-existing-secret\n')
        for _ in range(2):
            self.assertEqual(self.run_hook(REPAIR).returncode, 0)
        self.assertEqual(self.calls(), ['unshare', 'chown', '-hR', '0:0', '--', str(self.state)] * 2)
        self.assertEqual(config.read_text(), 'secret: keep-existing-secret\n')
        self.assertLess(REPAIR.name, '05pullimages')

    def test_missing_state_is_noop(self):
        self.state.rmdir()
        self.assertEqual(self.run_hook(REPAIR).returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_missing_environment_fails_closed(self):
        del self.env['AGENT_STATE_DIR']
        self.assertNotEqual(self.run_hook(REPAIR).returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_repair_failure_stops_action(self):
        self.env['PODMAN_RC'] = '1'
        self.assertNotEqual(self.run_hook(REPAIR).returncode, 0)

    def test_enabled_service_is_restarted_even_if_inactive(self):
        self.assertEqual(self.run_hook(RESTART).returncode, 0)
        self.assertEqual(self.calls(), ['--user', '--quiet', 'is-enabled', 'eturnal.service',
                                       '--user', 'restart', 'eturnal.service'])

    def test_unconfigured_service_is_not_started(self):
        self.env['ENABLED_RC'] = '1'
        self.assertEqual(self.run_hook(RESTART).returncode, 0)
        self.assertNotIn('restart', self.calls())

    def test_restart_failure_is_reported(self):
        self.env['RESTART_RC'] = '1'
        self.assertNotEqual(self.run_hook(RESTART).returncode, 0)


if __name__ == '__main__':
    unittest.main()
