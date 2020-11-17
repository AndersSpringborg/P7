const CracoLessPlugin = require("craco-less");

module.exports = {
  plugins: [
    {
      plugin: CracoLessPlugin,
      options: {
        lessLoaderOptions: {
          lessOptions: {
            modifyVars: {
              "@primary-color": "#360000",
              "@layout-header-background": "#360000",
              "@layout-trigger-background": "#400000",
            },
            javascriptEnabled: true,
          },
        },
      },
    },
  ],
};
