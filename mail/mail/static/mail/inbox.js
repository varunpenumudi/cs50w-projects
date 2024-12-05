document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector("#email-content-view").style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Submit composition form
  document.querySelector('#compose-form').onsubmit = () => {

    const email_obj = {
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value,
    };

    fetch('/emails', {method: 'POST', body:JSON.stringify(email_obj) })
    .then(response => response.json())
    .then(message => {
      console.log(message);
      load_mailbox('sent');
    });

    return false;
  }

}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector("#email-content-view").style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  
  // Clear out any existing contents in mailbox view
  document.querySelector('#emails-view').innerHTML = '';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  // GET request to emails/<mailbox>
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    emails.forEach(email => {
      const email_preview_box = document.createElement('div');
      email_preview_box.className = 'email_preview_box';

      email_preview_box.innerHTML = 
      `<div class='d-flex flex-row justify-content-between'> 
        <div class='font-weight-bold mr-3'> ${email.sender} </div> 
        <div> ${ email.subject } </div>
      </div> 
      <div class='font-weight-light'> ${email.timestamp} </div>`;

      // if the email is read then show in gray background box.
      if (email.read) {
        email_preview_box.style.backgroundColor = 'gray';
      }

      // add the box to emails view
      document.querySelector('#emails-view').append(email_preview_box);

      // Show the email if a email_preview_box is clicked
      email_preview_box.addEventListener('click', () => {
        const mailbox = document.querySelector('h3').innerHTML;
        show_email(email.id, mailbox);
      });

    });
    
  });
}



function show_email(email_id, mailbox) {

  // Show email content view and hide other views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector("#email-content-view").style.display = 'block';

  fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // Show email details
    document.querySelector("#email-sender").innerHTML = `<strong> From: </strong> ${email.sender}`;
    document.querySelector("#email-recipients").innerHTML = `<strong> To: </strong> ${email.recipients}`;
    document.querySelector("#email-subject").innerHTML = `<strong> Subject: </strong> ${email.subject}`;
    document.querySelector("#email-timestamp").innerHTML = `<strong> Timestamp: </strong> ${email.timestamp}`;

    // Show email body
    document.querySelector("#email-body").innerHTML = `${email.body}`;


    // Show the Archive/Unarchive buttons based on the mailbox
    const archive_btn = document.querySelector('#archive-btn');
    const unarchive_btn = document.querySelector('#unarchive-btn');

    archive_btn.style.display = 'none';
    unarchive_btn.style.display = 'none';

    if (mailbox == 'Archive') {
      unarchive_btn.style.display = 'block';

      // Unarchive when clicked
      unarchive_btn.addEventListener('click', () => {
        fetch(`emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: false
          })
        })
        .then(result => {
          console.log(result);
          load_mailbox('inbox');
        });
      });
    } 
    else if (mailbox == 'Inbox') {
      archive_btn.style.display = 'block';

      // Archive when clicked
      archive_btn.addEventListener('click', () => {
        fetch(`emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: true
          })
        })
        .then(result => {
          console.log(result);
          load_mailbox('inbox');
        });
      });
    }


    // event listiner for reply button click 
    document.querySelector('#reply-btn').addEventListener('click', () => {
      const reply_mail_sender = email.sender;
      const reply_mail_subject = email.subject;
      const reply_mail_timestamp = email.timestamp;
      const reply_mail_body = email.body;
      const current_user = document.querySelector('h2').innerHTML;

      // open email compose form
      compose_email();

      // Prefill reciepient, subject and body.
      document.querySelector('#compose-recipients').value = `${reply_mail_sender}`;
      if (reply_mail_subject.includes('Re:')) {
        document.querySelector('#compose-subject').value = `${reply_mail_subject}`;
      } else {
        document.querySelector('#compose-subject').value = `Re: ${reply_mail_subject}`;
      }
      const dividerline = '\n------------------------------------------------\n';
      document.querySelector('#compose-body').value = dividerline + `On ${reply_mail_timestamp} ${current_user} wrote: ${reply_mail_body} \n`;
    });


    // Mark email as Read
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    });
           
  });
}