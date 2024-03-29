# TF Easy Colors Map (Krita plugin)

#### Current version: 2.3 (11/11/2022)
____
#### • WHAT IS
TF Easy Colors Map is a plugin for Krita for creating a Map (a collection) of your favourite colors in a very simple way. The final result of your Map can be something like this:

![preview](https://i.ibb.co/QP9B3xY/colors.png)

It's not meant to be a replacement of the current Krita's colors management system, but just a super easy-to-use alternative system.
____
#### • HOW IT WORKS
All starts creating a new Colors Map, which is a simple text file with a .cmap extension. Now, you can start adding your colors, naming them and organizing them in collapsible / hideable Groups.
Adding a colors is pretty simple: once you have the desired color set in the Krita document **foreground**, just **right** click your Map, type a name when requested and it's added to your collection.

![preview](https://i.ibb.co/YTBJrkk/schema.jpg)

TIP: To add a color in a specific position, just **right** click with the **SHIFT** button pressed.

![preview](https://i.ibb.co/W5mV8XH/schema5.jpg)

If you need to catch more colors (for example, grabbing them from an image) you can automize the process. Just press the "Auto Add Colors" button and start using the Krita's Color Sampler tool to select your desired color. Every time the foreground color changes, the Colors Map will ask you to type a name and that color is added into your Map. When you finished, press the "Auto Add Colors" button again to stop this feature.

![preview](https://i.ibb.co/RhJLxfc/anim.gif)

____
#### • SELECT A COLOR FROM YOUR MAP

In your Map, just **left** click a color and your Krita document **foreground** color is set to that color. 

TIP: if you click with the **SHIFT** button pressed, the Krita document **background** color is set instead.

![preview](https://i.ibb.co/p3FRr8c/schema2.jpg)

____
#### • MANAGE YOUR MAP

You can perform various operations to manage your colors, names and grouped colors. For example, you can rename colors and group titles, move a color in a different position, delete a color or a group, and so on.
Just **right** click with the **CTRL** button pressed and a popup menu appears with all the available functionalities.

![preview](https://i.ibb.co/r02X5ZQ/schema3.jpg)

____
#### • OPEN/CLOSE, SHOW/HIDE, CUSTOMIZE THE COLORS GROUPS

- Groups can be opened and closed (collapsed) so that you can focus only on the colours you need to use in that moment. Just click the [+] / [-] icon on the right of each Groups title.
- Moreover, you can show and hide the Groups, making them visible or unvisible. Click the "Settings" button and check/uncheck the groups.
- Finally, you can change the background color and the text colors of the Groups so as to make the view more confortable for you eyes. Click the "Settings" button and specify two colors, as HTML code, in the dedicated field.

![preview](https://i.ibb.co/rw35vj0/color-openclose.png)
____
#### • COLORS SLOTS

Imagine you have a Group containing all the colors of a character. Your character has some "fixed" colors like, for example, hair, eyes and skin colors. He also has a set of different colors, for example, if he wears a uniform or some dresses.

![preview](https://i.ibb.co/fGcVFpz/immagine.png)

In a complex scenario where the Group has many colors, it's not so convenient to show them all together. For example, if you are coloring pages where the character is dressed in uniform, having the colors of the various dresses is useless and may be annoying. The use of Colors Slots resolves this scenario.

Just CTRL + right click a Color and select one of the available Slots from the menu. The "Main Slot" is intented for the colors you want always visible (hair, eyes and skin colors, for example). The other 5 Slots are intented for creating special "sub collections".

![preview](https://i.ibb.co/BfgB0cv/immagine.png)

For example, you can group all the Uniform colors into the Slot 1, the dresses colors in Slot 2 and Slot 3. Now, in the Main Slot you have only the "shared" colors. To show the colors into the Slot, just left click on the Group's Slot icon on the right and, from the menu, select the Slot you want to activate.

![preview](https://i.ibb.co/qRH48Rm/immagine.png)

For example, if you click Slot 1, you will see the "shared" colors (hair, eyes, skin) and the Uniform colors (the colors names are shown in italic):

![preview](https://i.ibb.co/Qm9W3b3/immagine.png)

In any moment, you can click "Main Slot" to shown the "shared" colors only or "Show All" for showing all the Group colors.
____
#### • TEMPORARY COLORS (SECONDARY PALETTE)

If you need to use a color, but you don't need to have it saved into your Colors Map, you can use the "secondary" palette placed under the Colors Map. 

![preview](https://i.ibb.co/Lrs2hK7/schema4.jpg)

In that palette, colors are kept in memory and not saved. It can be useful, for example, if you have to use a specific color more times in the current Krita document, but you don't need or want to have it in the Colors Map because it's used in that occasion only and it won't be used in other documents.
Adding and selecting colors here use the same logic of the Colors Map (but this palette doesn't have any functionality):
 - **right** click this palette for adding a color
 - **left** click a color to select it as foreground color (+ **SHIFT** as background color)

____
#### • POPUP PALETTE

You can easily access your palette by right clicking on your Krita document with the SHIFT button pressed.

![preview](https://i.ibb.co/Fh0T1yr/schema-6.png)
____
#### • YOUR KRITA DOCUMENT AND COLORS MAP ARE CONNECTED!

When you create a Colors Map, it's connected to your Krita document. This means that when you open your Krita document, your Colors Map will be automatically loaded.
____
#### • KRITA COLOR PROFILES SUPPORT (rgba, cmyka, YCbCrA, xyza, laba, graya)

When you add a color to your Colors Map, this plugin not only save the various channels value, but also the color characteristics: model, depth and profile. When you click a color, the plugin sends all these params to the Krita ManagedColors system, which returns a color corresponding to the given specifications.

This means that you can fill your Colors Map with colors coming from different profiles. For example, you can collect RGB, CMYK, GREY scale colors, all in the same Colors Map. However, because of the different nature of the various color profiles, this may raise some variations in your resulting color.

In conclusion, it's up to you creating Colors Maps with coherent profiles!

- CASE TEST

In the screenshot below, the Colors Map contains 3 colors: one with a CMYK profile, one with a LAB profile and the last one with a GRAY profile. Then, these colors have been used on 3 different Krita's Documents: a RGB, a CMYK and a LAB document.
As result, Krita has been able to reproduce (more or less) correctly the different colors in the different documents. Just the blue and the gray colors appear a little bit darker in the CMYK document.

![preview](https://i.ibb.co/hsJJC05/Colors-profile-TESTs.png)
____
#### • INLINE HELP MANUAL

Click the [?] button to show the inline manual with all the features explained.

____
#### • WHY THIS PLUGIN

I'm a comic artist, so I have to apply the same colors on different pages. Krita is fantastic software for the flattening process, but personally I find the color management system unsuitable for the flexibility and speed I would like. For this reason, I created a plugin that offered what I need, such as organizing colors quickly, easily seeing the name of a color and so on.

____
#### • WHAT'S NEW

#### 2.2 - 2.3 (11/11/2022)
 - New feature: Colors Slots
 - Bug: resolved a bug in the Colors Map popup window (colors where not properly selected)

#### 2.1 (21/09/2022)
 - New feature: you can customize the colors of the Groups bar.
 - Various code optimization

#### 2.0 (16/09/2022)
 - New plugin version

#### 0.1 (22/06/2022)
- Initial release
