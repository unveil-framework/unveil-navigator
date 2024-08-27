# UNVEIL Navigator

The UNVEIL Navigator is designed to provide basic navigation and annotation of [UNVEIL](https://unveilframework.net) matrices. UNVEIL Navigator is a modified version of MITRE ATT&CK Navigator with custom contents to include the UNVEIL matrix.

The navigator allows you to manipulate the cells in the matrix (color coding, adding a comment, assigning a numerical value, etc.).  We thought having a simple tool that everyone could use to visualize the matrix would help make it easy to use ATT&CK. The principal feature of the Navigator is the ability for users to define layers -custom views of the ATT&CK knowledge base- showing just those techniques for a specific custom or highlighting techniques a specific adversary has been known to use. Layers can be created interactively within the Navigator or generated programmatically and then visualized via the Navigator.

## Security note

> **Important Note:** Layer files uploaded when visiting our Navigator instance hosted on GitHub Pages are **NOT** being stored on the server side, as the Navigator is a client-side only application. However, we still recommend installing and running your own instance of the UNVEIL Navigator if your layer files contain any sensitive content.

## Deployment

UNVEIL Navigator is expected to be installed and run using Docker and Docker compose.
Instructions on how to install Docker in your system can be found in the official [Docker](https://www.docker.com/) website.

To run the navigator locally you can get the repository (either by cloning or downloading the latest release) and use Docker and Docker Compose:

```
$ docker compose up --build -d
```

This will start everything you need to start a new service locally in port 4200.

## Usage

You can read more about how to use the application itself in the [USAGE](/USAGE.md) document (which is mirrored in the in-app help page).
When viewing the Navigator in a browser, click on the **?** icon in the upper right corner to view the in-app documentation.

## Advanced features 

There are some advanced settings which can be configured. 

### Disabling Navigator Features

The `features` array in `nav-app/src/assets/config.json` lists Navigator features you may want to disable. Setting the `enabled` field on a feature in the configuration file will hide all control
elements related to that feature.

However, if a layer is uploaded with an annotation or configuration
relating to that feature it will not be hidden. For example, if `comments` are disabled the
ability to add a new comment annotation will be removed, however if a layer is uploaded with
comments present they will still be displayed in tooltips and and marked with an underline.

Features can also be disabled using the _create customized Navigator_ feature. Refer to the in-application help page section "Customizing the Navigator" for more details.
