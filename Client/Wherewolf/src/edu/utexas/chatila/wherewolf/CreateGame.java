package edu.utexas.chatila.wherewolf;

import edu.utexas.chatila.wherewolf.R;
import edu.utexas.chatila.wherewolf.R.id;
import edu.utexas.chatila.wherewolf.R.layout;
import edu.utexas.chatila.wherewolf.R.menu;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class CreateGame extends Activity {

	
	private class CreateGameTask extends AsyncTask<Void, Void, CreateGameResponse>{
		
		@Override
		protected  CreateGameResponse doInBackground(Void... request){
			
			WherewolfPreferences pref = new WherewolfPreferences(CreateGame.this);			
			final EditText gnameTV = (EditText) findViewById(R.id.gameName);
			final EditText descTV = (EditText) findViewById(R.id.gameDescription);
			
			String username = pref.getUsername();
			String password = pref.getPassword();
			String gamename = gnameTV.getText().toString();
			String description = descTV.getText().toString();
			
			
			//for (CreateGameResponse r : request)
			//{
				CreateGameRequest gameRequest = new CreateGameRequest(username, password, gamename, description);
				return gameRequest.execute(new WherewolfNetworking());
	          
			//}
				
		}
		
		protected void onPostExecute(CreateGameResponse params){
			
	          final TextView errorText = (TextView) findViewById(R.id.error_text);

			
			if (params.getStatus().equals("success"))
			{
				int gameID = params.getGameID();
				WherewolfPreferences pref = new WherewolfPreferences(CreateGame.this);			
				pref.setCurrentGameID(gameID);
				
				Context context = getApplicationContext();
				CharSequence text = "You have created a game.";
				int duration = Toast.LENGTH_LONG;

				Toast toast = Toast.makeText(context, text, duration);
				startGameLobby();
				toast.show();

			}else{
				
				errorText.setText(params.getErrorMessage());			}
		}
	}
	private int startGameLobby(){
		Intent intent = new Intent(this, GameLobby.class);
		startActivity(intent);
		return 9;
	}
	
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_create_game);
		
		final Button button = (Button) findViewById(R.id.createGame);

		View.OnClickListener game = new View.OnClickListener() {
			public void onClick(View v) {
				new CreateGameTask().execute();
			}
		};
		
		button.setOnClickListener(game);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.create_game, menu);
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
