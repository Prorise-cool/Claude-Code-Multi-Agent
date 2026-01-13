export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation changes
        'style',    // Code style changes (formatting, missing semicolons, etc.)
        'refactor', // Code refactoring (neither fixes a bug nor adds a feature)
        'perf',     // Performance improvements
        'test',     // Adding or updating tests
        'build',    // Build system or external dependency changes
        'ci',       // CI/CD configuration changes
        'chore',    // Other changes that don't modify src or test files
        'revert'    // Revert a previous commit
      ]
    ],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-case': [2, 'always', 'sentence-case'],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 100],
    'body-leading-blank': [2, 'always'],
    'body-max-line-length': [2, 'always', 100],
    'footer-leading-blank': [2, 'always']
  }
};
