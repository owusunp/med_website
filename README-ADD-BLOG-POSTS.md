# How to add a new blog post (card) using the Python helper

This guide is for anyone who needs to add a new article to the site **without editing code by hand**. The small program `add_blog_post.py` opens a form on your computer. When you fill it out and click Submit, it **saves your new post into the real `page-html.html` file on your Mac**—the one inside your project folder (e.g. under **Documents**). That file on disk is updated immediately; the **live website** does not change until you copy that file into Squarespace (Step 5).

These instructions assume you are on a **Mac**. (If you use Windows, the ideas are the same—use **Command Prompt** instead of Terminal and **`python`** instead of **`python3`** where noted.)

The helper is a normal desktop window. To copy the updated file into Squarespace you can use **TextEdit** (Mac’s built-in app) if you want to open the file first—or paste straight from the file into Squarespace’s Code block.

The add-post tool only edits files inside a folder on your computer. 

---

## Get the project folder

You need a copy of the website project that includes at least `add_blog_post.py` and the `squarespace` folder inside it.

After unzipping, open the folder until you see the file **`add_blog_post.py`** listed. The **`squarespace`** folder should sit **in the same folder** as that file (not moved elsewhere). If the ZIP created an extra wrapper folder (e.g. `med_website-main`), that is fine—as long as `add_blog_post.py` and `squarespace` are together inside whatever folder you use.

**Good place to put it:** Your **Documents** folder is fine, e.g. `Documents/med_website`. The exact name does not matter.

---

## What you need on your Mac

1. **Python 3** installed.  
   - Check: press **Cmd + Space**, type **Terminal**, press **Enter**. In the Terminal window, type exactly:
     ```text
     python3 --version
     ```
     and press **Enter**.  
   - If you see something like `Python 3.11.x`, you are set.  
   - If you see `command not found` or an error, install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/) (download the macOS installer, open the `.pkg`, click through Next). After installing, **quit and reopen Terminal**, then run `python3 --version` again.

2. **That project folder** saved somewhere you can find in **Finder** (for example **Documents → med_website**). Do not move `add_blog_post.py` away from the `squarespace` folder.

---

## Step 1: Open the helper (Mac)

Double-clicking `add_blog_post.py` in Finder often **does not** run the program—it may open the file in an editor instead. Use **Terminal** and the steps below; you only need to do this once per session.

### 1. Open the project folder in Finder

1. Click the **Finder** icon in the Dock (the smiling face).
2. In the menu bar, click **Go → Home** (or press **Cmd + Shift + H**).
3. Open **Documents** (or wherever you put the project).
4. Open the project folder until you see **`add_blog_post.py`** in the window. **Leave this Finder window open**—you will use it in the next step.

### 2. Open Terminal

1. Press **Cmd + Space** (hold Command, tap Space).
2. Type **Terminal**.
3. Press **Enter**.  
   A window with a prompt (often your name and a `%` or `$`) will appear.

### 3. Go to the project folder without typing the path by hand

“Go to the folder” here means: tell Terminal to work inside the same folder where `add_blog_post.py` lives.

1. In the **Terminal** window, type **`cd`** then **press the Space bar once** (you should see `cd ` with a space after it). **Do not press Enter yet.**
2. Switch to **Finder**, click the **folder icon** in the title bar of the window that contains `add_blog_post.py` (or click the folder name in the path bar at the bottom of the Finder window if you use that view). You want the **folder that directly contains** `add_blog_post.py`, not the file itself.
3. **Drag that folder** from Finder into the **Terminal** window and **drop** it on the line where you typed `cd `.  
   Terminal will fill in the full path for you, something like:
   ```text
   cd /Users/yourname/Documents/med_website
   ```
4. Press **Enter**.  
   If nothing looks wrong, you are now “in” the project folder.

### 4. Run the script

In the same Terminal window, type exactly:

```text
python3 add_blog_post.py
```

Press **Enter**.

A window titled **“Add Blog Post - Squarespace”** should open. You can scroll the form if your screen is small.

**If Terminal says `command not found` for `python3`:** Install Python from python.org (see “What you need” above), then close Terminal, open it again, and repeat from step 3.

---

## Step 2: Fill out the form (what each part does)

| Field | What it is | Where it shows on the website |
|--------|------------|--------------------------------|
| **Date (e.g. Mar 15)** | Full date string for display | On the **card** and in the **article** header area |
| **Month (e.g. Mar)** | Short month | Used with **Day** for the date pill on the **card** |
| **Day (e.g. 15)** | Day of month | Same as above |
| **Title** | Headline of the post | **Card** title and **article** page title |
| **Author** | Byline name | **Card** and **article**; also used to look up a short bio if you add one |
| **Author Bio (optional)** | One or two sentences about the author | **Article** view only (author area), not the small card grid |
| **Categories** | One or more checkboxes | Controls **which category page** lists this post and **filtering**. If you pick nothing, it defaults to “The Nitty-Gritty” |
| **Excerpt** | Short preview text | **Card** teaser text under the title (not the full article) |
| **Image** | Either **Upload from computer** *or* paste a **URL** | **Card** thumbnail and **article** hero image. Upload embeds the image directly in the file (no separate hosting step for that image) |
| **Aspect Ratio** | Usually leave **82%** | How tall the image area is on the **card** / **article** (padding trick for responsive images) |
| **Article content** | The full post | Appears only when someone **clicks** the card to read the article. Write in normal paragraphs; **blank lines** become new paragraphs. You can paste a line that is **only** an image URL to drop in a picture between paragraphs |

**Required before Submit:** Title, Author, Excerpt, Image (upload or URL), and Article content. The script will pop up a warning if something required is missing.

---

## Step 3: Submit

Click the blue button **“Submit — Add Post to Squarespace”**.

**What just happened:** The program **rewrote** `page-html.html` on your laptop—the copy in **squarespace → Custom Code**. You can open that file in Finder right after and see it is newer / larger. Nothing was uploaded to Squarespace or the internet by this step alone.

**Do you need to save?** **No.** The helper saves the file for you—there is nothing to **Cmd + S** in the form window (it is not a document editor). You do **not** need to open `page-html.html` first just to “save” the new post.

**Only if you already had `page-html.html` open** in TextEdit or another app before you ran the helper: that window may still show the **old** text until you **reload** or close and reopen the file. Do **not** press **Cmd + S** there on the old version, or you could wipe out the new post the script just wrote.

- If everything works, you will see a **Success** message. It reminds you which file was updated and what to do next in Squarespace (see below).
- The program will close after success. If you see an error, read the message—it often means the expected file was moved or renamed.

---

## Step 4: Where your new post was written (for your peace of mind)

The script **does not** send anything to the internet by itself. It only edits a **local file** on your computer:

**Inside your project folder, the path is:** `squarespace` → `Custom Code` → `page-html.html`

So from Finder: open your project folder → **squarespace** → **Custom Code** → **`page-html.html`**.

Inside that file, your new post is added in **three** conceptual places (you do not need to edit these by hand if you use the form):

1. **`postsData`** — A list of “card” records: date, title, author, categories, excerpt, image, etc. This is what builds the **grid of cards** on the home page and category sections.

2. **`articleBodies`** — The **full article HTML** for when a visitor opens that post. The script assigns the next number (index) automatically so it matches the new card.

3. **`authorBios`** (only if you filled **Author Bio**) — Short blurbs keyed by author name, used in the **article** layout when that author is shown.

So: **cards** come from `postsData`; **clicking a card** loads the matching entry from `articleBodies`.

---

## Step 5: Getting the change onto Squarespace

The live site does not update until you **copy the updated code** into Squarespace:

1. In **Finder**, go to your project folder → **squarespace** → **Custom Code**.
2. **Right-click** `page-html.html` → **Open With** → **TextEdit** (or another plain text editor you prefer).  
   - If TextEdit shows a formatting toolbar and behaves like a word processor, use the menu **Format → Make Plain Text** before saving, so you do not accidentally save rich text. For a quick copy-paste to Squarespace, you can also select all and copy without changing much—as long as you are copying the raw file contents.
3. With the file open, press **Cmd + A** (select all), then **Cmd + C** (copy).
4. In Squarespace, on the website page, click edit. Then click anywhere on the page and click the pencil.
5. Click into the **Code** block and paste (**Cmd + V**). Use **HTML** mode if the block asks for a mode.
6. **Save** the page in Squarespace.

**Important if you already had `page-html.html` open in TextEdit while you ran the script:** TextEdit may ask to reload the file from disk because it changed—click **Revert** or reload. If you save an old version without reloading, you could **overwrite** the new post.

---

## Tips for non-programmers

- **Backups:** Before big updates, duplicate `page-html.html` somewhere safe (another folder, USB drive, email to yourself, etc.).
- **Quotes in titles:** Avoid straight double quotes (`"`) inside titles or excerpts if you can; the script tries to escape them, but simple text is safest.
- **Images:** For a URL, use a full address starting with `https://`. Uploaded images are stored as long text inside the HTML file—that is normal.
- **Order of posts:** New posts are appended in order; the site logic uses the **index** (position in the list) for links like `#article-5`.

---

## If something goes wrong

- **“File not found”** — `page-html.html` is not where the script expects. Make sure `add_blog_post.py` lives in the same project folder as the `squarespace` folder (see “Get the project folder” above).
- **“Could not find postsData” / “articleBodies”** — The HTML file may have been edited and those names changed. Restore from a backup or ask whoever maintains the code.
- **`python3: command not found`** — Install Python from [python.org](https://www.python.org/downloads/) for Mac, then open a **new** Terminal window and try again.

For questions about Squarespace blocks and publishing, use your site’s usual Squarespace workflow; this README only covers the **local** add-post tool and where it writes.
