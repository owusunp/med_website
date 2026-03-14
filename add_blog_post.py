#!/usr/bin/env python3
"""
Blog Post Editor - Add new posts to Squarespace page-html.html
Run: python add_blog_post.py
Double-click add_blog_post.py on Mac/Windows (if Python is installed)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import os
import re
import base64
from html import escape as html_escape

# Path to page-html.html (relative to this script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PAGE_HTML_PATH = os.path.join(SCRIPT_DIR, "squarespace", "Custom Code", "page-html.html")

CATEGORIES = ["The Nitty-Gritty", "Roadmap", "Admissions", "Resources", "Mentor Spotlight"]

# Global for image upload (set in main)
uploaded_image_var = None

MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def image_file_to_data_url(filepath):
    """Convert image file to base64 data URL."""
    ext = os.path.splitext(filepath)[1].lower()
    mime = MIME_TYPES.get(ext, "image/jpeg")
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"


def escape_js_template_literal(text):
    """Escape text for use inside JavaScript template literal (backticks)."""
    return text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


# Standalone line that is only an image URL (common extensions, optional query string)
IMAGE_URL_RE = re.compile(
    r"^\s*(https?://\S+\.(?:png|jpe?g|gif|webp)(?:\?\S*)?)\s*$",
    re.IGNORECASE,
)


def plain_text_to_html(text):
    """Convert plain text to HTML. Blank lines separate paragraphs.
    Any line that is only an image URL becomes an <img> (works after text too)."""
    text = text.strip()
    if not text:
        return ""
    # If it already looks like HTML, return as-is
    if text.strip().startswith("<"):
        return text
    lines = text.split("\n")
    html_parts = []
    paragraph_lines = []

    def flush_paragraph():
        if not paragraph_lines:
            return
        p = "<br>".join(paragraph_lines)
        html_parts.append(f"<p>{p}</p>")
        paragraph_lines.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            continue
        if IMAGE_URL_RE.match(stripped):
            flush_paragraph()
            url_attr = html_escape(stripped, quote=True)
            html_parts.append(f'<p class="article-body-image"><img src="{url_attr}" alt=""></p>')
            continue
        paragraph_lines.append(line.strip())
    flush_paragraph()
    return "".join(html_parts)


def add_post_to_file(data):
    """Append new post and article body to page-html.html."""
    if not os.path.exists(PAGE_HTML_PATH):
        messagebox.showerror("Error", f"File not found:\n{PAGE_HTML_PATH}")
        return False

    with open(PAGE_HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Categories from checkboxes
    cats = data["categories"]
    if not cats:
        cats = ["The Nitty-Gritty"]

    # Build post object string
    cats_str = "[" + ", ".join(f'"{c}"' for c in cats) + "]"
    post_entry = (
        f'  {{ date: "{data["date"]}", month: "{data["month"]}", day: "{data["day"]}", '
        f'title: "{data["title"].replace(chr(34), chr(92)+chr(34))}", '
        f'author: "{data["author"].replace(chr(34), chr(92)+chr(34))}", '
        f'categories: {cats_str}, '
        f'excerpt: "{data["excerpt"].replace(chr(34), chr(92)+chr(34)).replace(chr(10), " ")}", '
        f'image: "{data["image"]}", aspectRatio: "{data["aspect_ratio"]}" }}'
    )

    # Escape article body for template literal
    body_escaped = escape_js_template_literal(data["article_body"])

    # Find next index - count postsData entries
    posts_match = re.search(r"const postsData = \[(.*?)\];", content, re.DOTALL)
    if not posts_match:
        messagebox.showerror("Error", "Could not find postsData in file.")
        return False

    posts_content = posts_match.group(1)
    post_count = len(re.findall(r"\{ date:", posts_content))
    next_index = post_count

    # Do postsData first (later in file) so articleBodies positions don't shift
    # 1. Add to postsData - insert before ];
    posts_start = content.find("const postsData = [")
    posts_array_start = content.find("[", posts_start) + 1
    posts_array_end = content.find("];", posts_array_start)

    post_addition = f",\n  {post_entry}"
    content = content[:posts_array_end] + post_addition + content[posts_array_end:]

    # 2. Add to articleBodies - find the closing }; of articleBodies block
    article_bodies_start = content.find("const articleBodies = {")
    if article_bodies_start == -1:
        messagebox.showerror("Error", "Could not find articleBodies in file.")
        return False

    # Find the }; that closes articleBodies (first }; after the block start)
    search_start = article_bodies_start + len("const articleBodies = {")
    close_pos = content.find("};", search_start)
    if close_pos == -1:
        messagebox.showerror("Error", "Could not find articleBodies closing.")
        return False

    # Insert new article body before };
    # The last entry has no trailing comma - we need to add comma to it and add new entry
    # Find the last ` before }; in the articleBodies block
    block_content = content[article_bodies_start:close_pos]
    last_backtick = block_content.rfind("`")
    if last_backtick == -1:
        messagebox.showerror("Error", "Could not parse articleBodies structure.")
        return False

    insert_pos = article_bodies_start + last_backtick + 1
    # Insert: ,\n  N: `body`
    article_addition = f',\n  {next_index}: `{body_escaped}`'
    content = content[:insert_pos] + article_addition + content[insert_pos:]

    # 3. Add author to authorBios if bio provided
    if data.get("author_bio"):
        author_escaped = data["author"].replace('\\', '\\\\').replace('"', '\\"')
        bio_escaped = data["author_bio"].replace('\\', '\\\\').replace('"', '\\"')
        bios_match = re.search(r'const authorBios = (\{[^;]+\});', content)
        if bios_match:
            # Check if author already exists
            if f'"{data["author"]}"' not in bios_match.group(1) and f"'{data['author']}'" not in bios_match.group(1):
                # Add before closing };
                bios_end = content.find("};", content.find("const authorBios = "))
                # Insert ,"Author": "Bio" before };
                bio_addition = f',"{data["author"]}": "{bio_escaped}"'
                content = content[:bios_end] + bio_addition + content[bios_end:]

    with open(PAGE_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def submit():
    global uploaded_image_var
    # Get selected categories from checkboxes
    selected_cats = [cat for cat, var in category_vars.items() if var.get()]
    if not selected_cats:
        selected_cats = ["The Nitty-Gritty"]

    # Image: use uploaded (data URL) or pasted URL
    img = uploaded_image_var.get().strip() or image_var.get().strip()
    data = {
        "date": date_var.get().strip(),
        "month": month_var.get().strip(),
        "day": day_var.get().strip(),
        "title": title_var.get().strip(),
        "author": author_var.get().strip(),
        "author_bio": author_bio_var.get().strip(),
        "categories": selected_cats,
        "excerpt": excerpt_text.get("1.0", tk.END).strip(),
        "image": img,
        "aspect_ratio": aspect_var.get().strip() or "82%",
        "article_body": plain_text_to_html(article_body_text.get("1.0", tk.END).strip()),
    }

    # Validate
    if not data["title"]:
        messagebox.showwarning("Missing field", "Please enter a title.")
        return
    if not data["author"]:
        messagebox.showwarning("Missing field", "Please enter an author.")
        return
    if not data["excerpt"]:
        messagebox.showwarning("Missing field", "Please enter an excerpt.")
        return
    if not data["image"]:
        messagebox.showwarning("Missing field", "Please upload an image or paste an image URL.")
        return
    if not data["article_body"]:
        messagebox.showwarning("Missing field", "Please enter the article body (HTML).")
        return

    if add_post_to_file(data):
        messagebox.showinfo(
            "Success",
            "Post added successfully!\n\n"
            "Updated file:\n" + PAGE_HTML_PATH + "\n\n"
            "• If page-html.html is open in your editor: reload it (e.g. use 'Revert File' or accept 'File changed on disk') so you see the new post. Don't save without reloading or you'll overwrite the changes.\n\n"
            "• Copy the code from that file and paste it into your Squarespace Code block.",
        )
        root.quit()
    else:
        messagebox.showerror("Error", "Failed to add post. Check the file path.")


def choose_image_file():
    """Open file dialog and set image to base64 data URL."""
    global uploaded_image_var
    path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.gif *.webp"),
            ("All files", "*.*"),
        ],
    )
    if path:
        try:
            data_url = image_file_to_data_url(path)
            uploaded_image_var.set(data_url)
            image_var.set("")  # Clear URL field when using upload
            image_label_var.set(f"✓ Loaded: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image:\n{e}")


def main():
    global root, date_var, month_var, day_var, title_var, author_var, author_bio_var
    global excerpt_text, image_var, image_label_var, uploaded_image_var
    global aspect_var, article_body_text, category_vars

    category_vars = {}
    root = tk.Tk()
    root.title("Add Blog Post - Squarespace")
    root.geometry("720x850")
    root.resizable(True, True)

    # Scrollable container so Submit button is always reachable
    canvas = tk.Canvas(root, highlightthickness=0)
    scrollbar = ttk.Scrollbar(root, command=canvas.yview)
    scrollable = ttk.Frame(canvas)

    def _on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_canvas_configure(event):
        canvas.itemconfig(canvas_window_id, width=event.width)

    def _on_mousewheel(event):
        # Windows: delta=±120, Mac: delta=±2-4 (use directly), Linux: Button-4/5
        if hasattr(event, "delta"):
            d = event.delta
            if abs(d) > 100:  # Windows
                d = d // 120
            canvas.yview_scroll(int(-1 * d), "units")
        elif event.num == 4:
            canvas.yview_scroll(-3, "units")
        elif event.num == 5:
            canvas.yview_scroll(3, "units")

    canvas_window_id = canvas.create_window((0, 0), window=scrollable, anchor="nw")
    scrollable.bind("<Configure>", _on_frame_configure)
    canvas.bind("<Configure>", _on_canvas_configure)
    canvas.configure(yscrollcommand=scrollbar.set)

    def _bind_scroll(e):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)

    def _unbind_scroll(e):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", _bind_scroll)
    canvas.bind("<Leave>", _unbind_scroll)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    main = ttk.Frame(scrollable, padding=20)
    main.pack(fill=tk.BOTH, expand=True)

    ttk.Label(main, text="Add New Blog Post", font=("", 16, "bold")).pack(pady=(0, 15))

    # Date fields
    date_frame = ttk.Frame(main)
    date_frame.pack(fill=tk.X, pady=5)
    ttk.Label(date_frame, text="Date (e.g. Mar 15):", width=20).pack(side=tk.LEFT, padx=(0, 10))
    date_var = tk.StringVar(value="Mar 15")
    ttk.Entry(date_frame, textvariable=date_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)

    month_frame = ttk.Frame(main)
    month_frame.pack(fill=tk.X, pady=5)
    ttk.Label(month_frame, text="Month (e.g. Mar):", width=20).pack(side=tk.LEFT, padx=(0, 10))
    month_var = tk.StringVar(value="Mar")
    ttk.Entry(month_frame, textvariable=month_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)

    day_frame = ttk.Frame(main)
    day_frame.pack(fill=tk.X, pady=5)
    ttk.Label(day_frame, text="Day (e.g. 15):", width=20).pack(side=tk.LEFT, padx=(0, 10))
    day_var = tk.StringVar(value="15")
    ttk.Entry(day_frame, textvariable=day_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Title
    ttk.Label(main, text="Title:").pack(anchor=tk.W, pady=(10, 0))
    title_var = tk.StringVar()
    ttk.Entry(main, textvariable=title_var, width=80).pack(fill=tk.X, pady=2)

    # Author
    ttk.Label(main, text="Author:").pack(anchor=tk.W, pady=(10, 0))
    author_var = tk.StringVar(value="Candid Premed")
    ttk.Entry(main, textvariable=author_var, width=80).pack(fill=tk.X, pady=2)

    # Author Bio (optional - for author card in article view)
    ttk.Label(main, text="Author Bio (optional):").pack(anchor=tk.W, pady=(10, 0))
    author_bio_var = tk.StringVar()
    ttk.Entry(main, textvariable=author_bio_var, width=80).pack(fill=tk.X, pady=2)

    # Categories (checkboxes)
    ttk.Label(main, text="Categories (select one or more):").pack(anchor=tk.W, pady=(10, 0))
    cat_frame = ttk.Frame(main)
    cat_frame.pack(fill=tk.X, pady=2)
    for cat in CATEGORIES:
        v = tk.BooleanVar(value=(cat == "The Nitty-Gritty"))
        category_vars[cat] = v
        cb = ttk.Checkbutton(cat_frame, text=cat, variable=v)
        cb.pack(side=tk.LEFT, padx=(0, 15))

    # Excerpt
    ttk.Label(main, text="Excerpt (short preview):").pack(anchor=tk.W, pady=(10, 0))
    excerpt_text = scrolledtext.ScrolledText(main, height=3, width=80, wrap=tk.WORD)
    excerpt_text.pack(fill=tk.X, pady=2)

    # Image - upload or URL
    ttk.Label(main, text="Image:").pack(anchor=tk.W, pady=(10, 0))
    img_frame = ttk.Frame(main)
    img_frame.pack(fill=tk.X, pady=2)
    ttk.Button(img_frame, text="Upload from computer", command=choose_image_file).pack(
        side=tk.LEFT, padx=(0, 10)
    )
    uploaded_image_var = tk.StringVar()  # Stores data URL when uploaded
    image_label_var = tk.StringVar(value="(No image selected)")
    ttk.Label(img_frame, textvariable=image_label_var, foreground="gray").pack(side=tk.LEFT)
    ttk.Label(main, text="Or paste image URL:").pack(anchor=tk.W, pady=(5, 0))
    image_var = tk.StringVar()
    ttk.Entry(main, textvariable=image_var, width=80).pack(fill=tk.X, pady=2)

    # Aspect ratio
    ttk.Label(main, text="Aspect Ratio (default 82%):").pack(anchor=tk.W, pady=(10, 0))
    aspect_var = tk.StringVar(value="82%")
    ttk.Entry(main, textvariable=aspect_var, width=20).pack(fill=tk.X, pady=2)

    # Article body - plain text, no code needed
    ttk.Label(
        main,
        text="Article content (write normally — no code needed; blank lines = new paragraphs):",
    ).pack(anchor=tk.W, pady=(10, 0))
    article_body_text = scrolledtext.ScrolledText(main, height=8, width=80, wrap=tk.WORD)
    article_body_text.pack(fill=tk.X, pady=2)
    article_body_text.insert(
        tk.END,
        "Your opening paragraph here. Write as you normally would.\n\n"
        "Section heading or second paragraph. Use blank lines to separate paragraphs.\n\n"
        "Takeaway: Your key point or lesson learned.",
    )

    # Submit button - prominent, always visible
    submit_frame = ttk.Frame(main)
    submit_frame.pack(fill=tk.X, pady=25)
    submit_btn = tk.Button(
        submit_frame,
        text="Submit — Add Post to Squarespace",
        command=submit,
        font=("", 13, "bold"),
        bg="#0d47a1",
        fg="white",
        activebackground="#1565c0",
        activeforeground="white",
        padx=24,
        pady=6,
        cursor="hand2",
        relief=tk.RAISED,
        borderwidth=2,
    )
    submit_btn.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
