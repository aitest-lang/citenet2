// e:\computer\CiteNet\citeNet\static\js\search_suggestion.js
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const suggestionsList = document.getElementById('suggestionsList');
    const suggestionsDiv = document.getElementById('suggestions');
    const submit = document.getElementById('submit');


    let selected = null;


    // Function to fetch search suggestions from an external API
    async function fetchSuggestions(query) {
        if (!query) {
            suggestionsDiv.style.display = 'none';
            return;
        }

        try {
            // Replace this URL with the actual external API endpoint
            const response = await fetch(`https://api.semanticscholar.org/graph/v1/paper/autocomplete?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            // Assuming the API returns an object with a "matches" array
            displaySuggestions(data.matches);
        } catch (error) {
            console.error('Error fetching suggestions:', error);
        }
    }

    // Function to display suggestions in the UI
    function displaySuggestions(matches) {
        suggestionsList.innerHTML = ''; // Clear previous suggestions

        if (matches && matches.length > 0) {
            matches.forEach(match => {
                const li = document.createElement('li'); // Create a new <li> element
                li.classList.add(
                    'px-4',
                    'py-2',
                    'cursor-pointer',
                    'bg-gray-800', // Darker grey background
                    'text-white',  // White text
                    'hover:bg-gray-600', // Slightly lighter grey background on hover
                    'transition', // Smooth transition for hover effect
                    'duration-200', // Duration of the transition
                    'rounded', // Rounded corners for each item
                    'flex', // Flexbox for alignment
                    'items-center', // Center items vertically
                    'animate-slide-in' // Apply the sliding animation
                );

                li.textContent = `${match.title} (${match.authorsYear})`; // Display title and authorsYear

                // Add click event listener to handle selection
                li.addEventListener('click', () => {
                    searchInput.value = match.title; // Update input with the selected title
                    suggestionsDiv.style.display = 'none'; // Hide suggestions

                    // Send the selected ID to the backend
                    selected = match.id;
                });

                suggestionsList.appendChild(li); // Append the <li> to the <ul>
            });

            suggestionsDiv.style.display = 'block'; // Show the suggestions container
        } else {
            suggestionsDiv.style.display = 'none'; // Hide the suggestions container if no matches
        }
    }

    // Function to send the selected ID to the backend
    async function sendSearchIdToBackend(id) {
        const csrfToken = getCookie('csrftoken'); // Get CSRF token
        try {
            const response = await fetch('/save-search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Add CSRF token to the headers
                },
                body: JSON.stringify({ id: id }) // Send the ID to the backend
            });

            if (response.ok) {
                console.log('Search ID saved successfully');
                // Redirect to the tree page after successful save
                window.location.href = '/tree';
            } else {
                console.error('Failed to save search ID');
            }
        } catch (error) {
            console.error('Error sending search ID to backend:', error);
        } finally {
             removeLoadingOverlay();//remove the loading screen
        }
    }

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Listen for input changes and fetch suggestions
    searchInput.addEventListener('input', (event) => {
        const query = event.target.value;
        fetchSuggestions(query);
        selected = null; // Reset selected id when typing
    });
    searchInput.addEventListener('focus', (event) => {
        const query = event.target.value;
        fetchSuggestions(query);
    });

    // Hide suggestions when clicking outside
    submit.addEventListener('click', (event) => {
         event.preventDefault(); // Prevent the default form submission
         if (selected) {
             sendSearchIdToBackend(selected);
         }else{
             console.log("please select an id")
         }
    });
});
