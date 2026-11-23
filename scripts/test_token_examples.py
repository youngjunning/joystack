"""Execute the documented capture example; do not infer Agent or token savings."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = ROOT / 'skills/engineering/joy-token/references/optimization.md'


class TokenCaptureExamplesTests(unittest.TestCase):
    def test_original_exit_and_complete_log_survive_output_filtering(self):
        examples = [code for code in re.findall(r'`([^`]+)`', DOCUMENT.read_text())
                    if '2>&1;' in code and code.endswith('=$?')]
        self.assertEqual(len(examples), 1, 'Expected one executable exit-capture example')
        capture = examples[0]
        result_variable = capture.rsplit(';', 1)[1].strip().split('=')[0]
        for name, flags in [('bash', ['--noprofile', '--norc']), ('zsh', ['-f'])]:
            shell = shutil.which(name)
            if shell is None:
                continue
            for original_exit in (0, 7):
                with self.subTest(shell=name, original_exit=original_exit):
                    with tempfile.TemporaryDirectory(prefix='joy-token-test-') as directory:
                        directory = Path(directory)
                        fixture = directory / 'input.log'
                        log = directory / 'captured.log'
                        fixture.write_text('INFO before\n' * 4000 +
                                           'ERROR middle failure\n' + 'INFO after\n' * 4000)
                        code = '\n'.join([
                            'fixture=$1; log=$2; original_exit=$3',
                            'task_command() { cat "$fixture"; printf "stderr detail\\n" >&2; return "$original_exit"; }',
                            capture,
                            'grep -n ERROR "$log"',
                            f'printf "original_exit=%s\\n" "${result_variable}"',
                        ])
                        result = subprocess.run(
                            [shell, *flags, '-c', code, 'capture-test', str(fixture),
                             str(log), str(original_exit)],
                            capture_output=True, text=True, timeout=10,
                        )
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertIn(f'original_exit={original_exit}\n', result.stdout)
                        self.assertIn('4001:ERROR middle failure', result.stdout)
                        self.assertEqual(log.read_text(), fixture.read_text() + 'stderr detail\n')
                        self.assertLess(len(result.stdout), 200)
        if not any(shutil.which(name) for name in ('bash', 'zsh')):
            self.skipTest('No supported shell available')


if __name__ == '__main__':
    unittest.main()
