           Front Matter | Jekyll • Simple, blog-aware, static sites                 {"@context":"https://schema.org","@type":"BlogPosting","dateModified":"2025-10-14T07:58:38-07:00","datePublished":"2025-10-14T07:58:38-07:00","description":"Any file that contains a YAML front matter block will be processed by Jekyll as a special file. The front matter must be the first thing in the file and must take the form of valid YAML set between triple-dashed lines. Here is a basic example:","headline":"Front Matter","image":"https://jekyllrb.com/img/jekyll-og.png","mainEntityOfPage":{"@type":"WebPage","@id":"https://jekyllrb.com/docs/front-matter/"},"publisher":{"@type":"Organization","logo":{"@type":"ImageObject","url":"https://jekyllrb.com/img/logo-2x.png"}},"url":"https://jekyllrb.com/docs/front-matter/"}

[Jekyll ![Jekyll Logo](/img/logo-2x.png)](/)
=============================================

*   [Home](/)
*   [Docs](/docs/)
*   [Resources](/resources/)
*   [Showcase](/showcase/)
*   [News](/news/)

*   [v4.4.1](https://github.com/jekyll/jekyll/releases/tag/v4.4.1)
*   [GitHub](https://github.com/jekyll/jekyll)

*   [Home](/)
*   [Docs](/docs/)
*   [Resources](/resources/)
*   [News](/news/)
*   [GitHub](https://github.com/jekyll/jekyll)

Navigate the docs… Quickstart Installation Ruby 101 Community Step by Step Tutorial Command Line Usage Configuration Rendering Process Pages Posts Front Matter Collections Data Files Assets Static Files Directory Structure Liquid Variables Includes Layouts Permalinks Themes Pagination Plugins Blog Migrations Upgrading Deployment

 [Improve this page](https://github.com/jekyll/jekyll/edit/master/docs/_docs/front-matter.md)

Front Matter
============

Any file that contains a [YAML](https://yaml.org/) front matter block will be processed by Jekyll as a special file. The front matter must be the first thing in the file and must take the form of valid YAML set between triple-dashed lines. Here is a basic example:

    ---
    layout: post
    title: Blogging Like a Hacker
    ---


Between these triple-dashed lines, you can set predefined variables (see below for a reference) or even create custom ones of your own. These variables will then be available for you to access using Liquid tags both further down in the file and also in any layouts or includes that the page or post in question relies on.

##### UTF-8 Character Encoding Warning

If you use UTF-8 encoding, make sure that no `BOM` header characters exist in your files or very, very bad things will happen to Jekyll. This is especially relevant if you’re running [Jekyll on Windows](/docs/installation/windows/).

##### Front Matter Variables Are Optional

If you want to use [Liquid tags and variables](/docs/variables/) but don’t need anything in your front matter, just leave it empty! The set of triple-dashed lines with nothing in between will still get Jekyll to process your file. (This is useful for things like CSS and RSS feeds!)

Predefined Global Variables
---------------------------

There are a number of predefined global variables that you can set in the front matter of a page or post.

Variable

Description

`layout`

If set, this specifies the layout file to use. Use the layout file name without the file extension. Layout files must be placed in the `_layouts` directory.

*   Using `null` will produce a file without using a layout file. This is overridden if the file is a post/document and has a layout defined in the [front matter defaults](/docs/configuration/front-matter-defaults/).
*   Starting from version 3.5.0, using `none` in a post/document will produce a file without using a layout file regardless of front matter defaults. Using `none` in a page will cause Jekyll to attempt to use a layout named "none".

`permalink`

If you need your processed blog post URLs to be something other than the site-wide style (default `/year/month/day/title.html`), then you can set this variable and it will be used as the final URL.

`published`

Set to false if you don’t want a specific post to show up when the site is generated.

##### Render Posts Marked As Unpublished

To preview unpublished pages, run \`jekyll serve\` or \`jekyll build\` with the \`--unpublished\` switch. Jekyll also has a handy [drafts](/docs/posts/#drafts) feature tailored specifically for blog posts.

Custom Variables
----------------

You can also set your own front matter variables you can access in Liquid. For instance, if you set a variable called `food`, you can use that in your page:

    ---
    food: Pizza
    ---

    <h1>{{ page.food }}</h1>


Predefined Variables for Posts
------------------------------

These are available out-of-the-box to be used in the front matter for a post.

Variable

Description

`date`

A date here overrides the date from the name of the post. This can be used to ensure correct sorting of posts. A date is specified in the format `YYYY-MM-DD HH:MM:SS +/-TTTT`; hours, minutes, seconds, and timezone offset are optional.

`category`

`categories`

Instead of placing posts inside of folders, you can specify one or more categories that the post belongs to. When the site is generated the post will act as though it had been set with these categories normally. Categories (plural key) can be specified as a [YAML list](https://en.wikipedia.org/wiki/YAML#Basic_components) or a space-separated string.

`tags`

Similar to categories, one or multiple tags can be added to a post. Also like categories, tags can be specified as a [YAML list](https://en.wikipedia.org/wiki/YAML#Basic_components) or a space-separated string.

##### Don't repeat yourself

If you don't want to repeat your frequently used front matter variables over and over, define [defaults](/docs/configuration/front-matter-defaults/ "Front Matter defaults") for them and only override them where necessary (or not at all). This works both for predefined and custom variables.

#### Getting Started

*   [Quickstart](/docs/)
*   [Installation](/docs/installation/)
*   [Ruby 101](/docs/ruby-101/)
*   [Community](/docs/community/)
*   [Step by Step Tutorial](/docs/step-by-step/01-setup/)

#### Build

*   [Command Line Usage](/docs/usage/)
*   [Configuration](/docs/configuration/)
*   [Rendering Process](/docs/rendering-process/)

#### Content

*   [Pages](/docs/pages/)
*   [Posts](/docs/posts/)
*   [Front Matter](/docs/front-matter/)
*   [Collections](/docs/collections/)
*   [Data Files](/docs/datafiles/)
*   [Assets](/docs/assets/)
*   [Static Files](/docs/static-files/)

#### Site Structure

*   [Directory Structure](/docs/structure/)
*   [Liquid](/docs/liquid/)
*   [Variables](/docs/variables/)
*   [Includes](/docs/includes/)
*   [Layouts](/docs/layouts/)
*   [Permalinks](/docs/permalinks/)
*   [Themes](/docs/themes/)
*   [Pagination](/docs/pagination/)

#### Guides

*   [Plugins](/docs/plugins/)
*   [Blog Migrations](/docs/migrations/)
*   [Upgrading](/docs/upgrading/)
*   [Deployment](/docs/deployment/)

Jekyll is lovingly maintained by the [core team](/team/) of volunteers.

The contents of this website are
© 2025 under the terms of the [MIT License](https://github.com/jekyll/jekyll/blob/master/LICENSE).
