# 🚀 QUICK START GUIDE - InsureGuard AI

## For Complete Beginners - Step by Step

### What You Need
- A computer with a web browser (Chrome, Firefox, Safari, or Edge)
- The project files (already downloaded)

---

## ⚡ FASTEST WAY TO TEST (5 Minutes)

### Step 1: Open the File
1. Find the folder where you downloaded the project files
2. Look for a file called `index.html`
3. **Double-click** on `index.html`
4. Your default web browser will open the website

### Step 2: Explore the Landing Page
- You'll see the homepage with features
- Try clicking the **moon/sun icon** in the top-right to change themes
- Try clicking the **palette icon** to change colors
- Scroll down to see all features

### Step 3: Submit a Test Claim
1. Click the **"Submit Your Claim"** button
2. You'll see three upload boxes

### Step 4: Upload Test Files
You need to upload 3 files. Here's how to create quick test files:

**For Voice File:**
- Use any MP3 file you have (like a song or voice memo)
- Or record a quick voice memo on your phone and transfer it

**For Image File:**
- Use any photo from your phone or computer (JPG or PNG)

**For Text File:**
- Open Notepad (Windows) or TextEdit (Mac)
- Type anything (e.g., "This is a test claim")
- Save as `test.txt`

### Step 5: Complete Submission
1. Upload all 3 files
2. Check the "I agree" checkbox
3. Click **"Submit for Analysis"**

### Step 6: Watch the Magic!
- You'll see an animated loading screen
- Watch as each file is "analyzed" (it's simulated)
- After a few seconds, you'll see the results

### Step 7: View Results
- See the overall score circle
- Read the detailed analysis for each file
- Try downloading the report

**That's it! You've tested the entire app! 🎉**

---

## 🔧 BETTER WAY (Using a Local Server)

For the best experience, use a local web server:

### If You Have Python (Most Macs and Linux have it)

1. **Open Terminal/Command Prompt**
   - Mac: Press `Cmd + Space`, type "Terminal", press Enter
   - Windows: Press `Win + R`, type "cmd", press Enter
   - Linux: Press `Ctrl + Alt + T`

2. **Navigate to Project Folder**
   ```bash
   cd path/to/insurance-fraud-detector
   ```
   
   Replace `path/to/insurance-fraud-detector` with your actual path.
   
   **Tip:** You can drag the folder into the terminal to auto-fill the path!

3. **Start Server**
   ```bash
   python3 -m http.server 8000
   ```
   
   Or if that doesn't work:
   ```bash
   python -m SimpleHTTPServer 8000
   ```

4. **Open Browser**
   - Open your web browser
   - Type in address bar: `http://localhost:8000`
   - Press Enter

5. **Done!** The app is now running.

6. **To Stop Server**
   - Go back to Terminal/Command Prompt
   - Press `Ctrl + C`

---

## 📝 Creating Test Files

### Voice File (Audio)
- **Option 1:** Use your phone's voice recorder, record anything, save as MP3
- **Option 2:** Download any MP3 file from your music library
- **Option 3:** Use an online voice recorder website and download the recording

### Image File (Photo)
- **Option 1:** Take a photo with your phone
- **Option 2:** Use any existing photo from your computer
- **Option 3:** Take a screenshot (it counts as an image!)
- **Supported formats:** JPG, PNG, WEBP

### Text File (Document)
**Windows:**
1. Right-click anywhere → New → Text Document
2. Name it `test.txt`
3. Open it and type anything
4. Save and close

**Mac:**
1. Open TextEdit
2. Type anything
3. File → Save As → Name it `test.txt`
4. Format: Plain Text

**Quick tip:** Any Word document, PDF, or text file works!

---

## 🎨 Customizing the App

### Change Default Theme
1. Open `config/app-config.js` in any text editor
2. Find line: `defaultTheme: 'dark',`
3. Change to: `defaultTheme: 'light',` for light mode
4. Save the file

### Change Default Color
1. Open `config/app-config.js`
2. Find line: `defaultAccentColor: 'blue',`
3. Change to any of: `'purple'`, `'green'`, `'orange'`, `'red'`, `'teal'`
4. Save the file

### Edit Features on Landing Page
1. Open `config/features-config.js`
2. You'll see a list of features
3. Edit the `title` and `description` of any feature
4. Save the file

---

## ❓ Common Questions

**Q: Can I use this without internet?**
A: Yes! The app works completely offline.

**Q: Is my data safe?**
A: Currently, all processing is simulated on your computer. Nothing is uploaded anywhere.

**Q: Can I change the colors?**
A: Yes! Click the palette icon in the top-right corner.

**Q: How do I reset everything?**
A: Just refresh the page (F5 or Cmd+R).

**Q: Why does the submit button stay gray?**
A: You must upload all 3 files AND check the terms checkbox.

**Q: Can I skip the loading animation?**
A: The analysis simulation is intentionally realistic. In a real deployment, this would show actual processing time.

---

## 🐛 Something Not Working?

### File Won't Upload
- Check the file type (must be the right format)
- Check file size (there are limits)
- Try a different file

### Page Looks Broken
- Try refreshing (F5 or Cmd+R)
- Try a different browser
- Make sure all files are in the correct folders

### Nothing Happens When I Click
- Check browser console (F12) for errors
- Make sure JavaScript is enabled
- Try a different browser

---

## 🎯 Next Steps

1. ✅ Test the basic functionality
2. ✅ Try different themes and colors
3. ✅ Edit the features in the config file
4. ✅ Read the full README for customization options
5. ✅ Integrate with your actual AI model API

---

## 📞 Need More Help?

Check these files:
- `README.md` - Full documentation
- `config/app-config.js` - App settings
- `config/features-config.js` - Feature content

**Congratulations! You're all set up! 🎊**

Now explore the code, make changes, and build something amazing!
