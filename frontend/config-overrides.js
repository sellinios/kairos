const { override, addWebpackModuleRule } = require('customize-cra');

module.exports = override(
  addWebpackModuleRule({
    test: /\.mjs$/,
    enforce: 'pre',
    use: ['source-map-loader'],
    exclude: /node_modules\/@react-aria\/ssr/,  // Exclude this module
  })
);
