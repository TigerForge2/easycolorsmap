# TF Easy Colors Map (Krita plugin)

#### Current version: 2.1 (21/09/2022)

#### WHAT IS
TF Easy Colors Map is a plugin for Krita for creating a Map (a collection) of your favourite colors in a very simple way. The final result of your Map can be something like this:

![preview](https://i.ibb.co/QP9B3xY/colors.png)

It's not meant to be a replacement of the current Krita's colors management system, but just a super easy-to-use alternative system.

#### HOW IT WORKS
All starts creating a new Colors Map, which is a simple text file with a .cmap extension. Now, you can start adding your colors, naming them and organizing them in collapsible / hideable Groups.
Adding a colors is pretty simple: once you have the desired color set in the Krita document **foreground**, just **right** click your Map, type a name when requested and it's added to your collection.

![preview](https://i.ibb.co/YTBJrkk/schema.jpg)

TIP: To add a color in a specific position, just **right** click with the **SHIFT** button pressed.

![preview](https://i.ibb.co/W5mV8XH/schema5.jpg)

If you need to catch more colors (for example, grabbing them from an image) you can automize the process. Just press the "Auto Add Colors" button and start using the Krita's Color Sampler tool to select your desired color. Every time the foreground color changes, the Colors Map will ask you to type a name and that color is added into your Map. When you finished, press the "Auto Add Colors" button again to stop this feature.

![preview](https://i.ibb.co/RhJLxfc/anim.gif)


#### SELECT A COLOR FROM YOUR MAP

In your Map, just **left** click a color and your Krita document **foreground** color is set to that color. 

TIP: if you click with the **SHIFT** button pressed, the Krita document **background** color is set instead.

![preview](https://i.ibb.co/p3FRr8c/schema2.jpg)


#### MANAGE YOUR MAP

You can perform various operations to manage your colors, names and grouped colors. For example, you can rename colors and group titles, move a color in a different position, delete a color or a group, and so on.
Just **right** click with the **CTRL** button pressed and a popup menu appears with all the available functionalities.

![preview](https://i.ibb.co/r02X5ZQ/schema3.jpg)

#### OPEN/CLOSE, SHOW/HIDE, CUSTOMIZE THE COLORS GROUPS

- Groups can be opened and closed (collapsed) so that you can focus only on the colours you need to use in that moment. Just click the [+] / [-] icon on the right of each Groups title.
- Moreover, you can show and hide the Groups, making them visible or unvisible. Click the "Settings" button and check/uncheck the groups.
- Finally, you can change the background color and the text colors of the Groups so as to make the view more confortable for you eyes. Click the "Settings" button and specify two colors, as HTML code, in the dedicated field.

![preview](https://i.ibb.co/rw35vj0/color-openclose.png)

#### TEMPORARY COLORS (SECONDARY PALETTE)

If you need to use a color, but you don't need to have it saved into your Colors Map, you can use the "secondary" palette placed under the Colors Map. 

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

#### KRITA COLOR PROFILES SUPPORT (rgba, cmyka, YCbCrA, xyza, laba, graya)

When you add a color to your Colors Map, this plugin not only save the various channels value, but also the color characteristics: model, depth and profile. When you click a color, the plugin sends all these params to the Krita ManagedColors system, which returns a color corresponding to the given specifications.

This means that you can fill your Colors Map with colors coming from different profiles. For example, you can collect RGB, CMYK, GREY scale colors, all in the same Colors Map. However, because of the different nature of the various color profiles, this may raise some variations in your resulting color.

In conclusion, it's up to you creating Colors Maps with coherent profiles!

- CASE TEST

In the screenshot below, the Colors Map contains 3 colors: one with a CMYK profile, one with a LAB profile and the last one with a GRAY profile. Then, these colors have been used on 3 different Krita's Documents: a RGB, a CMYK and a LAB document.
As result, Krita has been able to reproduce (more or less) correctly the different colors in the different documents. Just the blue and the gray colors appear a little bit darker in the CMYK document.

![preview](https://i.ibb.co/hsJJC05/Colors-profile-TESTs.png)

#### INLINE HELP MANUAL

Click the [?] button to show the inline manual with all the features explained.


#### WHY THIS PLUGIN

I'm a comic artist, so I have to apply the same colors on different pages. Krita is fantastic software for the flattening process, but personally I find the color management system unsuitable for the flexibility and speed I would like. For this reason, I created a plugin that offered what I need, such as organizing colors quickly, easily seeing the name of a color and so on.


#### WHAT'S NEW

#### 2.0 (16/09/2022)
 - New plugin version

#### 0.1 (22/06/2022)
- Initial release
