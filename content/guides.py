"""English guide pages, one per search intent. Keep them few and genuinely
useful (how-to first, product second); thin near-duplicates hurt rankings."""

GUIDES = [
    {
        "slug": "fix-motion-blur-photos",
        "title": "How to Fix Motion Blur in Photos (Free Tool + iPhone App)",
        "desc": "Fix shaky, motion-blurred photos: try the free in-browser motion blur fixer, learn why it happens, and get full-resolution AI results on iPhone.",
        "h1": "How to fix motion blur in photos",
        "intro": "Motion blur turns sharp edges into streaks. It happens when the camera or the subject moves while the shutter is open. The good news: because the streak follows one direction, motion blur is one of the easier kinds of blur to reverse.",
        "tool_mode": "motion",
        "body": """
<h2>Preview the fix in your browser</h2>
<p>Choose <strong>Motion blur</strong> in the tool above, then set the direction slider to match the streaks in your photo (0° for horizontal, 90° for vertical). Raise the strength until edges look crisp, and back off when you start to see halos or ripples.</p>
<ul>
  <li><strong>Direction matters most.</strong> If the result looks doubled, the angle is off. Try 15° steps.</li>
  <li><strong>Strength ≈ streak length.</strong> A 10-pixel smear needs a lower setting than a 30-pixel one.</li>
  <li><strong>Small, even blur works best.</strong> Classic deconvolution can't fix blur that curves (a twisting hand) or only affects part of the frame (a passing car).</li>
</ul>

<h2>Camera shake vs. subject motion</h2>
<div class="table-scroll"><table>
  <tr><th></th><th>Camera shake</th><th>Subject motion</th></tr>
  <tr><td>What moves</td><td>Your phone</td><td>The person, pet or car</td></tr>
  <tr><td>Looks like</td><td>The whole photo is smeared the same way</td><td>Background sharp, subject streaked</td></tr>
  <tr><td>Best fix</td><td>Motion blur mode or the app</td><td>The app: AI handles blur that only affects part of the frame</td></tr>
</table></div>

<h2>When to use the iPhone app instead</h2>
<p>Unblur Image's AI model doesn't need you to guess the angle, and it rebuilds texture such as hair, fabric and water that deconvolution can only sharpen. It also keeps your photo's full resolution. Use it for photos that matter: a once-only moment, a print, a profile picture.</p>
<p>Set <em>Safety Tolerance</em> low for a natural look and raise it for heavily smeared shots. With very heavy blur, the AI fills in plausible detail, so check faces before you print.</p>

<h2>How to avoid motion blur next time</h2>
<ol>
  <li><strong>Add light.</strong> In dim rooms the iPhone slows the shutter down; moving closer to a window helps more than any setting.</li>
  <li><strong>Brace the phone.</strong> Tuck your elbows in, or lean on a wall or table.</li>
  <li><strong>Use burst mode for action.</strong> Hold the shutter (or swipe it left on newer iPhones) and keep the sharpest frame.</li>
  <li><strong>Turn Night mode off for moving subjects.</strong> Long Night mode exposures blur anything that moves.</li>
  <li><strong>Turn on Live Photo,</strong> then pick a sharper key photo afterwards in Edit.</li>
</ol>
""",
        "faq": [
            ("Can motion blur be completely removed?", "Light, uniform blur can usually be reversed well. Heavy blur loses information that no tool can recover exactly. AI can rebuild a convincing version, but fine detail may differ from the original."),
            ("Why does my photo look worse after sharpening?", "Too much strength or the wrong direction creates halos and ripples. Lower the strength, or rotate the angle until the doubled edges disappear."),
        ],
        "related": ["fix-blurry-photos-on-iphone", "restore-old-blurry-photos"],
    },
    {
        "slug": "restore-old-blurry-photos",
        "title": "Restore Old Blurry Photos: Unblur Vintage Pictures with AI",
        "desc": "Bring old, soft and scanned family photos back to life. Scanning tips, a free online unblur preview, and AI restoration on iPhone.",
        "h1": "Restore old, blurry photos",
        "intro": "Old prints are rarely blurry for just one reason. Soft lenses, film grain, faded dyes and low-resolution scans all add up. A good restore starts with a good scan, then sharpens gently.",
        "tool_mode": "focus",
        "body": """
<h2>Step 1: Get the best possible scan</h2>
<ul>
  <li><strong>Use a flatbed scanner at 600 dpi</strong> (1200 dpi for wallet-size prints). Scanning resolution is detail you never have to invent later.</li>
  <li><strong>No scanner?</strong> Photograph the print in soft daylight with the phone held exactly parallel. Avoid the flash, which causes glare.</li>
  <li><strong>Clean the glass and the print</strong> with a soft, dry cloth. Dust looks like noise and gets sharpened along with everything else.</li>
  <li><strong>Remove the photo from glossy sleeves</strong> to avoid reflections.</li>
</ul>

<h2>Step 2: Sharpen gently</h2>
<p>Try the free tool above in <strong>Out of focus</strong> mode with a low strength (20–40). Old photos look fake when they are oversharpened. Stop as soon as eyes and hairlines read clearly.</p>

<h2>Step 3: Use AI for faces and lost detail</h2>
<p>Classic sharpening can only enhance edges that are still in the image. When a face is just a soft blob, the Unblur Image iPhone app uses an AI model to reconstruct plausible eyes, skin texture and hair, and keeps the full resolution of your scan. Start with a conservative <em>Safety Tolerance</em>; on family photos you want a result that still looks like grandma, not a stranger.</p>

<h2>Keep the original</h2>
<p>Always keep the untouched scan. Save the restored copy as PNG for printing or JPG for sharing, and label it as restored if you're building a family archive.</p>

<h2>What to expect</h2>
<div class="table-scroll"><table>
  <tr><th>Problem</th><th>Free tool</th><th>iPhone app (AI)</th></tr>
  <tr><td>Slightly soft print</td><td>Good</td><td>Very good</td></tr>
  <tr><td>Low-resolution scan</td><td>Limited</td><td>Good</td></tr>
  <tr><td>Face is a blur</td><td>Not enough</td><td>Rebuilds plausible detail</td></tr>
  <tr><td>Tears, scratches, colour fading</td><td>No</td><td>No (focused on blur)</td></tr>
</table></div>
""",
        "faq": [
            ("Will AI change how people in old photos look?", "It can. When a lot of detail is missing, the AI fills in a likely version. Use a conservative setting and compare with the original before you share or print."),
            ("Does the app fix scratches or colour?", "No. Unblur Image focuses on blur and sharpness. Retouch scratches and colour in a separate editor."),
        ],
        "related": ["fix-blurry-photos-on-iphone", "unblur-text-in-image"],
    },
    {
        "slug": "unblur-text-in-image",
        "title": "Unblur Text in an Image: Make Blurry Documents Readable",
        "desc": "Make blurry text readable: receipts, screenshots, whiteboards and documents. Free in-browser text sharpening plus AI on iPhone, and what is not possible.",
        "h1": "Unblur text in an image",
        "intro": "Blurry text is the most common ‘I just need to read this one thing’ problem: a receipt, a photographed page, a slide shot from the back of the room. Sharpening plus contrast often makes it legible.",
        "tool_mode": "text",
        "body": """
<h2>Try the Text mode</h2>
<p>Select <strong>Text</strong> in the tool above. It sharpens letter edges and stretches contrast so faint print stands out against the paper. Start around 50 and increase slowly; text turns blotchy when pushed too far.</p>
<ul>
  <li><strong>Crop first.</strong> Cropping to the paragraph you need gives the tool more pixels per letter.</li>
  <li><strong>For camera-shake streaks</strong> on a page, try <em>Motion blur</em> mode instead.</li>
  <li><strong>Pixelated screenshots</strong> (blocky, not soft) need AI upscaling. Use the app.</li>
</ul>

<h2>When the AI app helps</h2>
<p>Unblur Image's AI handles soft photos of documents, screenshots that look pixelated and whiteboard shots at full resolution. Keep the strength conservative: on text, an aggressive AI can “invent” a letter that looks right but isn't. <strong>Always double-check numbers, names and amounts</strong> against another source before relying on them.</p>

<h2>What can't be done</h2>
<p>No tool can honestly recover text that was deliberately blurred or pixelated to hide it, such as a redacted name or a censored licence plate. That information is gone, and anything an AI “reveals” is a guess. Unblur Image is meant for your own photos that came out soft by accident.</p>

<h2>Shoot documents sharper next time</h2>
<ol>
  <li>Use the Notes app's <em>Scan Documents</em> feature. It flattens the page and boosts contrast.</li>
  <li>Hold the phone parallel to the page and tap the text to focus.</li>
  <li>Avoid zooming in digitally; move closer instead.</li>
  <li>Use window light, not overhead lamps that cast your phone's shadow.</li>
</ol>
""",
        "faq": [
            ("Can I unblur a censored or pixelated name?", "No, and no honest tool can. Deliberate blurring removes the information; any ‘recovered’ text is made up."),
            ("What resolution do I need for readable text?", "As a rule of thumb, letters should be at least 15–20 pixels tall after cropping. Below that, sharpening alone rarely helps."),
        ],
        "related": ["fix-motion-blur-photos", "fix-blurry-photos-on-iphone"],
    },
    {
        "slug": "fix-blurry-photos-on-iphone",
        "title": "How to Fix Blurry Photos on iPhone (Causes, Fixes & App)",
        "desc": "Why iPhone photos come out blurry and how to fix them: lens, focus, low light, Portrait mode, iCloud thumbnails. Plus a free online fixer and an AI app.",
        "h1": "How to fix blurry photos on iPhone",
        "intro": "If your iPhone photos suddenly look soft, the cause is often something simple. Rule out these five first, then fix the photos you already have.",
        "tool_mode": "focus",
        "body": """
<h2>Five common causes and their fixes</h2>
<ol>
  <li><strong>A smudged lens.</strong> Pocket lint and fingerprints cause a soft, hazy look with glowing highlights. Wipe all the lenses with a microfibre cloth.</li>
  <li><strong>The wrong focus point.</strong> The camera focused on the background. Tap the subject before shooting; press and hold to lock focus (AE/AF Lock).</li>
  <li><strong>Too close.</strong> Every lens has a minimum focus distance. Newer iPhones switch to macro automatically; on older ones, step back and crop.</li>
  <li><strong>Low light.</strong> The shutter slows down, so hands and subjects blur. See our <a href="/fix-motion-blur-photos/">motion blur guide</a>.</li>
  <li><strong>It's an iCloud thumbnail.</strong> With “Optimize iPhone Storage” on, older photos show a low-resolution preview until the original downloads. Open the photo and wait for the progress circle to finish before judging it.</li>
</ol>
<p>Also check: a case or screen protector edge covering a lens, and Portrait mode depth effects that blur too much (open the photo, tap Edit → <em>f</em> and lower the effect).</p>

<h2>Fix a blurry photo you already took</h2>
<h3>Option 1: Photos app (built in)</h3>
<p>Edit → Adjust → <em>Sharpness</em> and <em>Definition</em>. This works for very slight softness but can't undo real blur.</p>
<h3>Option 2: Free online tool</h3>
<p>Use the tool on this page in Safari. It runs on your iPhone without uploading anything, and handles mild focus and motion blur.</p>
<h3>Option 3: Unblur Image app (AI)</h3>
<p>For noticeable blur, Unblur Image rebuilds lost detail with AI and keeps full resolution. Pick the photo, choose JPG/PNG/WebP, set the strength and tap <em>Remove Blur with AI</em>. Results save straight to Photos.</p>
""",
        "faq": [
            ("Why are my iPhone photos blurry all of a sudden?", "Usually a dirty or scratched lens, a case blocking the lens, or photos that are still iCloud thumbnails. If every photo is blurry even after cleaning, the camera module may need service."),
            ("Does Unblur Image work on iPad?", "Yes, it runs on iPhone and iPad with iOS 17.6 or later."),
        ],
        "related": ["fix-motion-blur-photos", "unblur-text-in-image"],
    },
    {
        "slug": "remini-alternative-ios",
        "title": "Remini Alternative for iPhone: Simple AI Blur Removal",
        "desc": "Looking for a Remini alternative on iOS? See how Unblur Image compares for fixing blurry photos, and try a free online unblur tool first.",
        "h1": "A simple Remini alternative for fixing blurry photos",
        "intro": "Remini is one of the best-known AI photo enhancers, especially for faces. If what you need is narrower, to take a blurry photo and make it sharp, a focused app can be simpler. Here's an honest comparison.",
        "tool_mode": "focus",
        "body": """
<h2>At a glance</h2>
<div class="table-scroll"><table>
  <tr><th></th><th>Unblur Image</th><th>Remini</th></tr>
  <tr><td>Focus</td><td>Removing blur from any photo: people, documents, landscapes</td><td>Broad AI enhancement with a strong focus on faces and portraits, plus extra creative features</td></tr>
  <tr><td>Platforms</td><td>iPhone & iPad (iOS 17.6+), plus a free browser tool on this site</td><td>iOS, Android and web</td></tr>
  <tr><td>Strength control</td><td>Conservative ↔ aggressive slider</td><td>Varies by feature</td></tr>
  <tr><td>Export formats</td><td>JPG, PNG, WebP</td><td>See the app</td></tr>
  <tr><td>Try before paying</td><td>Free online preview here, no account</td><td>See the app</td></tr>
</table></div>
<p class="small">Remini is a trademark of its owner. Features and prices change, so check each App Store page for current details. This page isn't affiliated with Remini.</p>

<h2>Choose Unblur Image if…</h2>
<ul>
  <li>Your problem is blur (shake, focus, soft scans), not retouching or style effects.</li>
  <li>You want to see a free preview before downloading anything.</li>
  <li>You fix documents and screenshots as well as portraits.</li>
  <li>You want to control how far the AI goes, so results stay natural.</li>
</ul>

<h2>Choose Remini if…</h2>
<ul>
  <li>You mainly enhance faces and want portrait-specific features.</li>
  <li>You need an Android app.</li>
</ul>

<h2>Try both on the same photo</h2>
<p>The fairest test is your own photo. Run it through the free tool above to see how much detail is recoverable, then compare both apps on the same image at the same resolution.</p>
""",
        "faq": [
            ("Is Unblur Image free?", "It's free to download, with a Premium subscription for unlimited restorations. The online tool on this site is free with no account."),
            ("Is there an Android version?", "Not yet. Android users can use the free online tool in the browser."),
        ],
        "related": ["fix-blurry-photos-on-iphone", "restore-old-blurry-photos"],
    },
]

TOOL_PAGE = {
    "slug": "free-unblur-tool",
    "title": "Free Online Unblur Tool – Sharpen Blurry Photos, No Upload",
    "desc": "Unblur photos online for free: focus, motion and text modes. Runs in your browser with no upload and no sign-up. Before/after preview, then full-resolution AI results in the iPhone app.",
    "h1": "Free online unblur tool",
    "intro": "Sharpen a blurry photo in your browser. Pick the blur type, adjust the strength and drag the slider to compare. Your photo never leaves your device.",
    "body": """
<h2>Which mode should I pick?</h2>
<ul>
  <li><strong>Out of focus:</strong> the whole picture is evenly soft, like a missed focus or a soft old print.</li>
  <li><strong>Motion blur:</strong> edges are smeared in one direction. Set the direction to match the streaks.</li>
  <li><strong>Text:</strong> documents, receipts and screenshots. Boosts edge contrast so letters are readable.</li>
</ul>
<h2>How it works</h2>
<p>The tool uses Richardson–Lucy deconvolution, a classic technique from astronomy imaging. It estimates how the blur spread each point of light, then reverses it step by step on the brightness channel, leaving colours untouched to avoid artifacts. It's fast and private, but it can only sharpen detail that is still present.</p>
<p>The Unblur Image iPhone app goes further: an AI model reconstructs lost detail in faces, hair and textures, and the result keeps your photo's original resolution.</p>
<h2>Limits of the free preview</h2>
<ul>
  <li>A low-resolution, watermarked preview that can't be saved. The full-quality result comes from the iPhone app.</li>
  <li>Works best on mild to moderate, uniform blur.</li>
  <li>Some browsers can't open HEIC; on iPhone, Safari can.</li>
</ul>
""",
    "faq": [
        ("Is my photo uploaded to a server?", "No. All processing happens in your browser using a Web Worker. You can even disconnect from the internet after the page loads."),
        ("Can I download the result?", "The online tool is a preview only: low resolution, watermarked and not downloadable. To save a full-resolution, watermark-free photo, use the free Unblur Image app for iPhone."),
    ],
}
