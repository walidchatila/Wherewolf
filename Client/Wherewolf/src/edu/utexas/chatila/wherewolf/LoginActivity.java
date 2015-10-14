package edu.utexas.chatila.wherewolf;

import edu.utexas.chatila.wherewolf.R;
import edu.utexas.chatila.wherewolf.R.id;
import edu.utexas.chatila.wherewolf.R.layout;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class LoginActivity extends Activity {

	private static final String TAG = "loginactivity";
	
	private class SigninTask extends AsyncTask<Void, Integer, SigninResponse> {
	      @Override
	      protected SigninResponse doInBackground(Void... request) {
	          // final EditText nameTV = (EditText) findViewById(R.id.usernameText);
	          // final EditText passTV = (EditText) findViewById(R.id.passwordText);
	          
	    	  
	    	  	final EditText nameTV = (EditText) findViewById(R.id.usernameText);
				final EditText passTV = (EditText) findViewById(R.id.passwordText);
				
				String username = nameTV.getText().toString();
				String password = passTV.getText().toString();
				
				SigninRequest signinRequest = new SigninRequest(username, password);
				return signinRequest.execute(new WherewolfNetworking());
	          
	          
	      
	      }
	      protected void onPostExecute(SigninResponse result) {
	          Log.v(TAG, "Signed in user has player id " + result.getPlayerID());
	          
	          final TextView errorText = (TextView) findViewById(R.id.error_text);
	          
	          /* result.geterrormessage - dump this response to this text field*/
	          
	          if (result.getStatus().equals("success")) {
	                          
	              final EditText nameTV = (EditText) findViewById(R.id.usernameText);
	              final EditText passTV = (EditText) findViewById(R.id.passwordText);
	              
	              WherewolfPreferences pref = new WherewolfPreferences(LoginActivity.this);
	              pref.setCreds(nameTV.getText().toString(), passTV.getText().toString());
	              errorText.setText("");
	              Log.v(TAG, "Signing in");
	              Intent intent = new Intent(LoginActivity.this, GameSelection.class);
	              startActivity(intent);
	              /* overridePendingTransition(R.anim.slide_in_right,
	                      R.anim.slide_out_left);  */
	          } else {
	              // do something with bad password
	              
	              errorText.setText(result.getErrorMessage());
	          }
	      }
	      
	  }
	
	      

	  

	private int startRegisterActivity(){
		Log.v(TAG, "User pressed the register button");
		Intent intent = new Intent(this, RegisterActivity.class);
		startActivity(intent);
		return 8;
	}
	
	private int startGameSelection(){
		Intent intent = new Intent(this, GameSelection.class);
		startActivity(intent);
		return 9;
	}
	
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_login);
		Log.i(TAG, "created the login activity");
		
		
		final Button button = (Button) findViewById(R.id.registerButton);

		View.OnClickListener reg = new View.OnClickListener() {
			public void onClick(View v) {
				startRegisterActivity();
			}
		};
		
		button.setOnClickListener(reg);
		
		final Button button1 = (Button) findViewById(R.id.loginButton);
		
		button1.setOnClickListener(new View.OnClickListener(){
			
			@Override
			public void onClick(View v){
				
				
				new SigninTask().execute();
			
				
			}
		});

		 /*(SharedPreferences sharedPref = getSharedPreferences("test", Context.MODE_PRIVATE);
		 SharedPreferences.Editor editor = sharedPref.edit();
		 String username = sharedPref.getString("username",null);
		 String password = sharedPref.getString("password",null);
		 Log.i(TAG, "username is " + username);
		 //editor.clear();
		 //editor.commit();
		 Log.i(TAG, "username is " + username);

		if (username != null && password !=null )
		{	Log.i(TAG, "username is " + username);
			startGameSelection();
			finish();}
		
		else{
			View.OnClickListener login = new View.OnClickListener() {
			public void onClick(View v) {
				SharedPreferences sharedPref = getSharedPreferences("test", Context.MODE_PRIVATE);
				SharedPreferences.Editor editor = sharedPref.edit();

				EditText usernameEdit = (EditText) findViewById(R.id.usernameText);
				EditText passwordEdit = (EditText) findViewById(R.id.passwordText);
				
				String username = usernameEdit.getText().toString();
				String password = passwordEdit.getText().toString();
				
				Log.i(TAG, "username is " + username);
				
				editor.putString("username", username);
				editor.putString("password", password);
				editor.commit();
				
				startGameSelection();
				finish();
			button1.setOnClickListener(login);
*/
		}

	
		
	@Override
	protected void onStart() {
		Log.i(TAG, "started the login activity");
		super.onStart();
		
		
	
		};	
	
		
	

	@Override
	protected void onRestart() {
		Log.i(TAG, "restarted the login activity");
		super.onRestart();
	}

	@Override
	protected void onResume() {
		Log.i(TAG, "resumed the login activity");
		super.onResume();
	}

	@Override
	protected void onPause() {
		Log.i(TAG, "pause the login activity");
		super.onPause();
	}

	@Override
	protected void onStop() {
		Log.i(TAG, "stopped the login activity");
		super.onStop();
	}

	@Override
	protected void onDestroy() {
		Log.i(TAG, "destroyed the login activity");
		super.onDestroy();
	}

	/*
	 * @Override public boolean onCreateOptionsMenu(Menu menu) { // Inflate the
	 * menu; this adds items to the action bar if it is present.
	 * getMenuInflater().inflate(R.menu.login, menu); return true; }
	 * 
	 * @Override public boolean onOptionsItemSelected(MenuItem item) { // Handle
	 * action bar item clicks here. The action bar will // automatically handle
	 * clicks on the Home/Up button, so long // as you specify a parent activity
	 * in AndroidManifest.xml. int id = item.getItemId(); if (id ==
	 * R.id.action_settings) { return true; } return
	 * super.onOptionsItemSelected(item); }
	 */
}