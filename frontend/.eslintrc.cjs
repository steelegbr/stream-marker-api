module.exports = {
    root: true,
    parser: '@typescript-eslint/parser',
    plugins: [
      '@typescript-eslint',
      'eslint-plugin-react',
      'eslint-plugin-react-hooks'
    ],
    extends: [
      'eslint:recommended',
      'plugin:@typescript-eslint/recommended',
      'plugin:eslint-plugin-react/recommended',
      'plugin:eslint-plugin-react-hooks/recommended'
    ],
  };