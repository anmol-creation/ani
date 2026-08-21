# .ac Ecosystem - Frontend Design

## 1. Overview
The frontend serves as the primary interface for the `.ac` Personal AI Assistant. It is designed to be lightweight, running locally and connecting to the FastAPI backend (`http://localhost:8000`). It is optimized for the Samsung DeX environment.

## 2. Tech Stack
* **HTML5:** Semantic structure.
* **CSS3 (Vanilla):** Styling with CSS variables for easy theming (Dark mode by default). No external CSS frameworks to keep it dependency-free and fast.
* **JavaScript (Vanilla/ES6):** Logic for API calls, DOM manipulation, and handling chat history. Uses the built-in `fetch` API.

## 3. UI Layout & Components
The layout will follow a modern chat interface style (similar to ChatGPT or Claude), tailored for desktop-like usage in Samsung DeX.

### Main View
* **Sidebar (Left - Optional for future expansion):**
  * Project/Session history list.
  * Settings button (to switch models later).
* **Chat Container (Center/Right):**
  * **Chat History Area:** Scrollable area displaying the conversation.
    * **User Message:** Distinct styling, aligned to the right.
    * **AI Response:** Distinct styling, aligned to the left.
    * **Sources Indicator:** A small tag or expandable section below the AI response showing which local files were referenced (e.g., *Sources: docs/design.md*).
  * **Input Area (Bottom):**
    * Textarea for typing messages (auto-expanding).
    * Send Button.
    * "Backend Status" indicator (Online/Offline).

## 4. API Integration
The frontend will communicate with the backend via REST APIs.

* **Endpoint:** `POST http://127.0.0.1:8000/chat`
* **Request Payload:**
  ```json
  { "message": "User query here" }
  ```
* **Response Handling:**
  ```json
  {
    "reply": "AI response here",
    "sources": ["source1.md", "source2.py"]
  }
  ```
* **Error Handling:** If the fetch fails (e.g., `Failed to fetch`), the UI will display a red alert indicating that the backend server needs to be started via Termux.

## 5. Theming & UX
* **Theme:** Deep Dark Mode (e.g., Background `#1e1e2e`, Surface `#181825`, Text `#cdd6f4`) inspired by Catppuccin or standard terminal colors.
* **Interactions:**
  * Pressing `Enter` sends the message.
  * Pressing `Shift + Enter` adds a new line in the textarea.
  * Auto-scroll to the bottom when a new message arrives.
  * Loading indicator (typing animation) while waiting for the AI response.
