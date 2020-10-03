const {createMessageAdapter} = require('@slack/interactive-messages');
const slackSigningSecret = '7d7f2de148bf44e7346d1ee6b6f67deb';
const slackInteractions = createMessageAdapter(slackSigningSecret, "/slack/events");
const port = 12109;

slackInteractions.action({type: 'url_verification'}, (payload, respond) => {
    // Logs the contents of the action to the console
    console.log('payload', payload);
    console.log(payload.getAllKeys());

    // Send an additional message to the whole channel
    doWork()
        .then(() => {
            respond({text: 'Thanks for your submission.'});
        })
        .catch((error) => {
            respond({text: 'Sorry, there\'s been an error. Try again later.'});
        });

    // If you'd like to replace the original message, use `chat.update`.
    // Not returning any value.
});


// Example of handling static select (a type of block action)
slackInteractions.action({type: 'static_select'}, (payload, respond) => {
    // Logs the contents of the action to the console
    console.log('payload', payload);

    // Send an additional message to the whole channel
    doWork()
        .then(() => {
            respond({text: 'Thanks for your submission.'});
        })
        .catch((error) => {
            respond({text: 'Sorry, there\'s been an error. Try again later.'});
        });

    // If you'd like to replace the original message, use `chat.update`.
    // Not returning any value.
});

// Example of handling all message actions
slackInteractions.action({type: 'message_action'}, (payload, respond) => {
    // Logs the contents of the action to the console
    console.log('payload', payload);

    // Send an additional message only to the user who made interacted, as an ephemeral message
    doWork()
        .then(() => {
            respond({text: 'Thanks for your submission.', response_type: 'ephemeral'});
        })
        .catch((error) => {
            respond({text: 'Sorry, there\'s been an error. Try again later.', response_type: 'ephemeral'});
        });

    // If you'd like to replace the original message, use `chat.update`.
    // Not returning any value.
});

// Example of handling all dialog submissions
slackInteractions.action({type: 'dialog_submission'}, (payload, respond) => {
    // Validate the submission (errors is of the shape in https://api.slack.com/dialogs#input_validation)
    const errors = validate(payload.submission);

    // Only return a value if there were errors
    if (errors) {
        return errors;
    }

    // Send an additional message only to the use who made the submission, as an ephemeral message
    doWork()
        .then(() => {
            respond({text: 'Thanks for your submission.', response_type: 'ephemeral'});
        })
        .catch((error) => {
            respond({text: 'Sorry, there\'s been an error. Try again later.', response_type: 'ephemeral'});
        });
});

// Example of handling attachment actions. This is for button click, but menu selection would use `type: 'select'`.
slackInteractions.action({type: 'button'}, (payload, respond) => {
    // Logs the contents of the action to the console
    console.log('payload', payload);

    // Replace the original message again after the deferred work completes.
    doWork()
        .then(() => {
            respond({text: 'Processing complete.', replace_original: true});
        })
        .catch((error) => {
            respond({text: 'Sorry, there\'s been an error. Try again later.', replace_original: true});
        });

    // Return a replacement message
    return {text: 'Processing...'};
});

(async () => {
    const server = await slackInteractions.start(port);
    console.log(`Listening for events on ${server.address().port}`);
})();