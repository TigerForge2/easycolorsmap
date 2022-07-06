# TF Easy Colors Map (Krita plugin)

#### Current version: 1.2 (06/07/2022)

#### WHAT IS
TF Easy Colors Map is a plugin for Krita for creating a Map (a collection) of your favourite colors in a very simple way. The final result of your Map can be something like this:

![preview](https://i.ibb.co/QP9B3xY/colors.png)

It's not meant to be a replacement of the current Krita's colors management system, but just a super easy-to-use alternative system.

#### HOW IT WORKS
All starts creating a new Colors Map, which is a simple .txt file. Now, you can start adding your colors and, if you want, organizing them with titles.
Adding a colors is pretty simple: once you have the desired color set in the Krita document **foreground**, just **right** click your Map, type a name when requested and it's added to your collection.

![preview](https://i.ibb.co/YTBJrkk/schema.jpg)

To add a color in a specific position, just **right** click with the **SHIFT** button pressed.

![preview](https://i.ibb.co/W5mV8XH/schema5.jpg)

If you need to catch more colors (for example, grabbing them from an image) you can automize the process. Just press the "Auto Add Colors" button and start using the Krita's Color Sampler tool to select your desired color. Every time the foreground color changes, the Colors Map will ask you to type a name and that color is added into your Map. When you finished, press the "Auto Add Colors" button again to stop this feature.

![preview](https://i.ibb.co/RhJLxfc/anim.gif)


#### SELECT A COLOR FROM YOUR MAP

In your Map, just **left** click a color and your Krita document **foreground** color is set to that color. Moreover, if you click with the **SHIFT** button pressed, the Krita document **background** color is set instead.

![preview](https://i.ibb.co/p3FRr8c/schema2.jpg)


#### MANAGE YOUR MAP

You can perform various operations to manage your colors, titles and grouped colors. For example, you can rename colors and titles, move a color in a different position, delete a color or a title, and so on. Just **right** click with the **CTRL** button pressed and a popup menu appears with all the available functionalities.

![preview](https://i.ibb.co/r02X5ZQ/schema3.jpg)


#### TEMPORARY COLORS (SECONDARY PALETTE)

If you need to use a color, but you don't need to have it saved into your Colors Map, you can use the "secondary" palette placed above the Colors Map. 

![preview](https://i.ibb.co/Lrs2hK7/schema4.jpg)

In that palette, colors are kept in memory and not saved. It can be useful, for example, if you have to use a specific color more times in the current Krita document, but you don't need or want to have it in the Colors Map because it's used in that occasion only and it won't be used in other documents.
Adding and selecting colors here use the same logic of the Colors Map (but this palette doesn't have any functionality):
 - **right** click this palette for adding a color
 - **left** click a color to select it as foreground color (+ **SHIFT** as background color)


#### POPUP PALETTE

You can easily access your palette by right clicking on your Krita document with the SHIFT button pressed.

![preview](https://i.ibb.co/Fh0T1yr/schema-6.png)

#### YOUR KRITA DOCUMENT AND COLORS MAP ARE CONNECTED!

When you create a Colors Map, it's connected to your Krita document. This means that when you open your Krita document, your Colors Map will be automatically loaded.

#### RGB & CMYK SUPPORTED

From this plugin point of view, a color is just a color. You can work with RGB and CMYK Krita documents without any particular precaution. You can even use the same Colors Map both in RGB and CMYK documents. 

#### INLINE HELP MANUAL

Click the [?] button to show the inline manual with all the features explained.


#### WHY THIS PLUGIN

I'm a comic artist, so I have to apply the same colors on different pages. Krita is fantastic software for the flattening process, but personally I find the color management system unsuitable for the flexibility and speed I would like. For this reason, I created a plugin that offered what I need, such as organizing colors quickly, easily seeing the name of a color and so on.


#### WHAT'S NEW

#### 1.2 (06/07/2022)
 - Resolved an issue when adding a new color from CMYK Krita documents. 

#### 1.1 (27/06/2022)
 - The "Easy Colors Map" palette is now available as a "pop-up palette" doing right-click + SHIFT on the Krita document.
 - Some improvements and bug fix

#### 1.0 (24/06/2022)
 - Krita document and Colors Map are now connected through a dedicated annotation.
 - Added the "left click" + CTRL action for renaming the clicked Color or Group Title.
 - The new "Settings" button allows to change the Colors size and the size of their names.
 - Support for RGB and CMYK color profiles.

#### 0.1 (22/06/2022)
Initial release
