package edu.utexas.chatila.wherewolf;

import edu.utexas.chatila.wherewolf.R;
import edu.utexas.chatila.wherewolf.R.id;
import edu.utexas.chatila.wherewolf.R.layout;
import edu.utexas.chatila.wherewolf.R.menu;
import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class RegisterActivity extends Activity {
	
	private static final String TAG = "registeractivity";
	
	private class RegisterTask extends AsyncTask<Void, Integer, CreateUserResponse> {
	      
		@Override
	      protected CreateUserResponse doInBackground(Void... request) {
	          // final EditText nameTV = (EditText) findViewById(R.id.usernameText);
	          // final EditText passTV = (EditText) findViewById(R.id.passwordText);
	          
	          	          
			final EditText nameTV = (EditText) findViewById(R.id.usernameText);
			final EditText passTV = (EditText) findViewById(R.id.passwordText);
			final EditText firstTV = (EditText) findViewById(R.id.firstName);
			final EditText lastTV = (EditText) findViewById(R.id.lastName);
			
			
			String username = nameTV.getText().toString();
			String password = passTV.getText().toString();
			String firstname = firstTV.getText().toString();
			String lastname = lastTV.getText().toString();
			
			CreateUserRequest registerrequest = new CreateUserRequest(username, password, firstname, lastname);
			return registerrequest.execute(new WherewolfNetworking());
	      
	      }
	      protected void onPostExecute(CreateUserResponse result) {
	          Log.v(TAG, "Signed in user has user id " + result.getuserID());
	          
	          final TextView errorText = (TextView) findViewById(R.id.error_text);
	          
	          /* result.geterrormessage - dump this response to this text field*/
	          
	          if (result.getStatus().equals("success")) {
	                          
	              final EditText nameTV = (EditText) findViewById(R.id.usernameText);
	              final EditText passTV = (EditText) findViewById(R.id.passwordText);
	              
	              WherewolfPreferences pref = new WherewolfPreferences(RegisterActivity.this);
	              pref.setCreds(nameTV.getText().toString(), passTV.getText().toString());
	              errorText.setText("");
	              Log.v(TAG, "Registering User");
	              finish();
	              /* overridePendingTransition(R.anim.slide_in_right,
	                      R.anim.slide_out_left);  */
	          } else {
	              // do something with bad password
	              
	              errorText.setText(result.getErrorMessage());
	          }
	      }
	      
	  }
	public void stopRegistering(){
		Log.v(TAG, "closing the register screen");
		this.finish();
	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_register);
	
		final Button button = (Button) findViewById(R.id.register_user_button);
		
		final Button button1 = (Button) findViewById(R.id.cancel_to_login);


		View.OnClickListener jim = new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				Log.v(TAG, "Register");
				
				new RegisterTask().execute();
			}
		};
		
		View.OnClickListener cancel = new View.OnClickListener() {
			public void onClick(View v) {
				Log.v(TAG, "CACNEL");

				stopRegistering();
				
			}
		};
		
		button.setOnClickListener(jim);
		button1.setOnClickListener(cancel);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.register, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}
}
