package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;
import java.util.List;

import edu.utexas.chatila.wherewolf.R;
import edu.utexas.chatila.wherewolf.R.id;
import edu.utexas.chatila.wherewolf.R.layout;
import edu.utexas.chatila.wherewolf.R.menu;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.AdapterView.OnItemClickListener;


public class GameSelection extends Activity {
	
	private static final String TAG = "gameselectionctivity";
	

	ArrayAdapter <Games> adapter;
	ArrayList <Games> nGames;
	int gameID;
	
	private int startLogin(){
		Intent intent = new Intent(this, LoginActivity.class);
		startActivity(intent);
		this.finish();
		return 9;
	}

	public void signout(){
		
		SharedPreferences sharedPref = getSharedPreferences("test", Context.MODE_PRIVATE);
		SharedPreferences.Editor editor = sharedPref.edit();
		String username = sharedPref.getString("username", "");
		Log.i(TAG, "username is " + username);

		editor.clear();
		editor.commit();
		
		Log.i(TAG, "username is " + username);


		startLogin();

	}
	private int startCreateGame(){
		Intent intent = new Intent(this, CreateGame.class);
		startActivity(intent);
		return 9;
	}
	
	private int startGameLobby(){
		Intent intent = new Intent(this, GameLobby.class);
		startActivity(intent);
		return 9;
	}
	
	private class GetGameTask extends AsyncTask<GetGameRequest, Integer, GetGameResponse>{
	
		@Override
		protected GetGameResponse doInBackground(GetGameRequest... params){
			WherewolfPreferences pref = new WherewolfPreferences(GameSelection.this);
			String username = pref.getUsername();
			String password = pref.getPassword();
			
			GetGameRequest getgameRequest = new GetGameRequest(username, password);
			return getgameRequest.execute(new WherewolfNetworking());
		}
	
		@Override
		protected void onPostExecute(GetGameResponse games){
			
			
			nGames = games.getGames();
			
			for (Games g : nGames){
				 
				Log.i(TAG, g + "games");
			}
			
			Log.i(TAG, "games " + nGames);

			adapter.clear();
			adapter.addAll(nGames);
			adapter.notifyDataSetChanged();
			
			ListView gameListView = (ListView) findViewById(R.id.games_list);
			gameListView.setAdapter(adapter);
			
			gameListView.setOnItemClickListener(new OnItemClickListener(){
			      public void onItemClick(      AdapterView<?> parent,      View v,      int position,      long id){
			      gameID = (nGames.get(position)).getGameId();
			        //startGameLobby();
			      }
			}
			);
		}

	
	}
	private class JoinGameTask extends AsyncTask<JoinGameRequest, Integer, JoinGameResponse>{
		
		@Override
		protected JoinGameResponse doInBackground(JoinGameRequest... params){
			WherewolfPreferences pref = new WherewolfPreferences(GameSelection.this);
			String username = pref.getUsername();
			String password = pref.getPassword();
			int gameid = gameID;
			
			
			JoinGameRequest JoinGameRequest = new JoinGameRequest(username, password, gameid);
			return JoinGameRequest.execute(new WherewolfNetworking());
		}
		
		@Override
		protected void onPostExecute(JoinGameResponse params){
			
			final TextView errorText = (TextView) findViewById(R.id.error_text);

			
			if (params.getStatus().equals("success"))
			{
				WherewolfPreferences pref = new WherewolfPreferences(GameSelection.this);			
				pref.setCurrentGameID(gameID);
				
				Context context = getApplicationContext();
				CharSequence text = "You have joined a game.";
				int duration = Toast.LENGTH_LONG;

				Toast toast = Toast.makeText(context, text, duration);
				startGameLobby();
				toast.show();

			}else{
				
				errorText.setText(params.getErrorMessage());	
		}
	}
	}
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_game_selection);
		Log.i(TAG, "started select activity");
		
		nGames = new ArrayList <Games>(); 
		adapter = new GameAdapter(this, nGames);
			
		final Button button = (Button) findViewById(R.id.CreateGameButton);
		final Button button1 = (Button) findViewById(R.id.JoinGameButton);

		View.OnClickListener create = new View.OnClickListener() {
			public void onClick(View v) {
				startCreateGame();
			}
		};
		
		View.OnClickListener join = new View.OnClickListener() {
			public void onClick(View v) {
				new JoinGameTask().execute();
				startGameLobby();
			}
		};
		
		
		button.setOnClickListener(create);
		button1.setOnClickListener(join);
	
		
	}
	
	@Override
	protected void onResume()
	{
		super.onResume();
		new GetGameTask().execute();
	}
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.game_selection, menu);
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
		if (id == R.id.sign_out){
			signout();
		}
		return super.onOptionsItemSelected(item);
	}
}
