# UNVEIL Navigator

The UNVEIL Navigator is designed to provide basic navigation and annotation of [UNVEIL](https://unveilframework.net) matrices, something that people are already doing today in tools like Excel.  We've designed it to be simple and generic - you can use the Navigator to visualize your defensive coverage, your red/blue team planning, the frequency of detected techniques or anything else you want to do.  The Navigator doesn't care - it just allows you to manipulate the cells in the matrix (color coding, adding a comment, assigning a numerical value, etc.).  We thought having a simple tool that everyone could use to visualize the matrix would help make it easy to use ATT&CK.

The principal feature of the Navigator is the ability for users to define layers - custom views of the ATT&CK knowledge base - e.g. showing just those techniques for a particular platform or highlighting techniques a specific adversary has been known to use. Layers can be created interactively within the Navigator or generated programmatically and then visualized via the Navigator.

## Usage

You can read more about how to use the application itself in the [USAGE](/USAGE.md) document (which is mirrored in the in-app help page).
Please see [Install and Run](#Install-and-Run) for information on how to get the VEIL Navigator set up locally.

**Important Note:** Layer files uploaded when visiting our Navigator instance hosted on GitHub Pages are **NOT** being stored on the server side, as the Navigator is a client-side only application. However, we still recommend installing and running your own instance of the VEIL Navigator if your layer files contain any sensitive content.

Use our [GitHub Issue Tracker](https://github.com/UNVEILFramework/unveil-navigator/issues) to let us know of any bugs or others issues that you encounter. We also encourage pull requests if you've extended the Navigator in a cool way and want to share back to the community!

*See [CONTRIBUTING.md](https://github.com/UNVEILFramework/attack-navigator/blob/master/CONTRIBUTING.md) for more information on making contributions to the UNVEIL Navigator.*

## Install and Run

To run the navigator locally you can clone the repository and use Docker and Docker Compose:

```
$ docker compose up --build -d
```

This will start everything you need to start a new service locally in port 4200.

## Supported Browsers

* Chrome
* Firefox
* Internet Explorer 11<sup>[1]</sup>
* Edge
* Opera
* Safari<sup>[2]</sup>

**[1]** There is a recorded issue with the SVG export feature on Internet Explorer. Because of a [missing functionality on SVGElements](https://developer.mozilla.org/en-US/docs/Web/API/ParentNode/children) in that browser, text will not be properly vertically centered in SVGs exported in that browser. We recommend switching to a more modern browser for optimal results.

**[2]** ATT&CK Navigator only supports Safari versions 14 and above because older versions of the browser can exhibit an unfixable freeze when selecting a layer tab. Users on unsupported versions of the browser will be warned of this possibility when opening the application.

## Documentation

When viewing the Navigator in a browser, click on the **?** icon in the upper right corner to view the in-app documentation.

## Disabling Navigator Features

The `features` array in `nav-app/src/assets/config.json` lists Navigator features you may want to disable. Setting the `enabled` field on a feature in the configuration file will hide all control
elements related to that feature.

However, if a layer is uploaded with an annotation or configuration
relating to that feature it will not be hidden. For example, if `comments` are disabled the
ability to add a new comment annotation will be removed, however if a layer is uploaded with
comments present they will still be displayed in tooltips and and marked with an underline.

Features can also be disabled using the _create customized Navigator_ feature. Refer to the in-application help page section "Customizing the Navigator" for more details.

## Embedding the Navigator in a Webpage

If you want to embed the Navigator in a webpage, use an iframe:

```HTML
<iframe src="https://mitre-attack.github.io/attack-navigator/enterprise/" width="1000" height="500"></iframe>
```

If you want to embed a version of the Navigator with specific features removed (e.g tabs, adding annotations), or with a default layer, we recommend using the _create customized Navigator_ feature. We highly recommend disabling the "leave site dialog" via this means when embedding the Navigator since otherwise you will be warned whenever you try to leave the embedding page. Refer to the in-application help page section "Customizing the Navigator" for more details.

The following is an example iframe which embeds our [*Bear APTs](layers/data/samples/Bear_APT.json) layer with tabs and the ability to add annotations removed:

```HTML
<iframe src="https://mitre-attack.github.io/attack-navigator/enterprise/#layerURL=https%3A%2F%2Fraw.githubusercontent.com%2Fmitre%2Fattack-navigator%2Fmaster%2Flayers%2Fdata%2Fsamples%2FBear_APT.json&tabs=false&selecting_techniques=false" width="1000" height="500"></iframe>
```