// craco.config.js
module.exports = {
  webpack: {
    configure: (webpackConfig) => {
      webpackConfig.module.rules.push({
        test: /\.mjs$/,
        enforce: 'pre',
        use: ['source-map-loader'],
        exclude: /node_modules\/@react-aria\/ssr/, // Exclude the problematic module
      });

      return webpackConfig;
    },
  },
};
