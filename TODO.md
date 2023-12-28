# Jarvis Assistant - Project To-Do List

## Completed Steps

1. **Voice Activation and Wake Word Detection**

   - Implement a system to continuously listen for the wake word "Jarvis" using Porcupine.

2. **Command Processing**

   - Develop `command_listener.py` to capture and process spoken commands after the wake word is detected.

3. **Speech Output (Text-to-Speech)**

   - Integrate text-to-speech functionality in `speech_output.py` for audible feedback and responses.

4. **Visual Indicator**

   - Create a visual indicator using Tkinter to display when Jarvis is active or listening.

5. **Command Execution**

   - Enable execution of specific commands such as opening applications and controlling Spotify.

6. **Integration with OpenAI API**

   - Integrate with the OpenAI API for handling queries and commands not directly executable by the system.

7. **Handling Specific Commands**

   - Set up the system to recognize and execute a variety of commands, including opening specific applications and controlling Spotify playback.

8. **GUI for Application Control**

   - Develop a basic GUI with an on/off toggle to control the Jarvis application.

9. **Refinement of OpenAI API Integration**

   - Update the system message for the OpenAI API to include specific command formats and instructions for the model to respond with exact commands when applicable.

10. **Expanding Command Functionality**

    - Enhance the `spotify_commands` function to handle additional Spotify-related tasks (playing specific playlists, adjusting volume, playing music by artists).

11. **Improving Response Handling**
    - Refine logic in `query_command` to better handle responses from the OpenAI API, ensuring correct execution or spoken responses based on content.

## Steps in Progress and Next Steps

12. **Expanding commands**

    - Add more commands such as: 
      - **Volume Control**
        - Increase or decrease the desktop volume.
        - Adjust the volume of specific applications.
      - **Web Browsing Assistance**
        - Open specific URLs or perform web searches.
        - Read out summaries of web articles.
      - **Weather Information**
        - Get current weather for a specific location.
        - Retrieve weather forecasts for a given date and location.
      - **System Utilities**
        - Check system status (CPU, memory usage).
        - Perform system actions like shutdown, restart, or sleep.
      - **Calendar and Reminders**
        - Add events to a calendar.
        - Set reminders for specific tasks or appointments.
      - **Email and Messaging**
        - Read unread emails from the inbox.
        - Send quick emails or messages through predefined templates.
      - **File and Folder Management**
        - Open specific files or folders.
        - Perform basic file operations like copy, move, delete.
      - **Smart Home Control**
        - Integrate with IoT devices to control lights, thermostats, etc.
        - Retrieve status updates from smart home devices.
      - **News and Information**
        - Fetch and read out the latest news headlines.
      - **Finance and Budgeting**
        - Give updates on stock prices or market news.
        - Assist in basic budgeting and expense tracking.
      - **Github integration**
         - Allow connection to Github to commit, push, etc.
         - Fetch information about PRs, information on a repository, etc.

13. **Debugging and Troubleshooting**

    - Address issues in response handling, particularly ensuring correct code execution based on the API's response.

14. **User Experience and Continuous Interaction**

    - Improve user experience by enhancing responsiveness and intuitiveness of interactions with Jarvis.
    - Implement more natural and continuous conversational capabilities.

15. **Testing and Refinement**

    - Systematically test the application to identify and fix bugs.
    - Refine features and interactions based on user feedback and testing results.

16. **Documentation and User Guide**

    - Create comprehensive documentation and a user guide explaining Jarvis's capabilities and interaction methods.

17. **Security and Privacy Enhancements**

    - Implement measures for user data privacy and security, especially for personal or sensitive information.

18. **Scalability and Additional Features**
    - Explore options to scale the application and add features, such as other service integrations or home automation controls.

