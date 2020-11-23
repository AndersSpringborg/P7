const CracoLessPlugin = require("craco-less");

module.exports = {
  plugins: [
    {
      plugin: CracoLessPlugin,
      options: {
        lessLoaderOptions: {
          lessOptions: {
            modifyVars: {
              "@primary-color": "#6D0000",
              "@layout-header-background": "#6D0000",
              "@layout-trigger-background": "#580000",
            },
            javascriptEnabled: true,
          },
        },
      },
    },
  ],
};
