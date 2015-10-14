package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;

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

public class GameLobby extends Activity {
	
	private static final String TAG = "Lobby";
	
	ArrayAdapter <Players> adapter;
	ArrayList <Players> nPlayers;

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
	
	private int startMainScreen(){
		Intent intent = new Intent(this, MainScreenActivity.class);
		startActivity(intent);
		return 9;
	}
	
	private int startGameSelection(){
		Intent intent = new Intent(this, GameSelection.class);
		startActivity(intent);
		return 9;
	}
	
	private class GetPlayerTask extends AsyncTask<GetPlayerRequest, Integer, GetPlayerResponse>{
		
		@Override
		protected GetPlayerResponse doInBackground(GetPlayerRequest... params){
			WherewolfPreferences pref = new WherewolfPreferences(GameLobby.this);
			String username = pref.getUsername();
			String password = pref.getPassword();
			int gameID	= pref.getCurrentGameID();
			
			GetPlayerRequest GetPlayerRequest = new GetPlayerRequest(username, password, gameID);
			return GetPlayerRequest.execute(new WherewolfNetworking());
		}
	
		@Override
		protected void onPostExecute(GetPlayerResponse games){
			
			
			nPlayers = games.getPlayers();
			for (Players g : nPlayers){
				 
				Log.i(TAG, g + "games");
			}
			
			Log.i(TAG, "games " + nPlayers);

			adapter.clear();
			adapter.addAll(nPlayers);
			adapter.notifyDataSetChanged();
			
			ListView gameListView = (ListView) findViewById(R.id.player_lobby_list);
			gameListView.setAdapter(adapter);
			
			gameListView.setOnItemClickListener(new OnItemClickListener(){
			      public void onItemClick(      AdapterView<?> parent,      View v,      int position,      long id){
			        startMainScreen();
			      }
			}
			);
		}

	
	}
	
private class LeaveGameTask extends AsyncTask<LeaveGameRequest, Integer, LeaveGameResponse>{
		
		@Override
		protected LeaveGameResponse doInBackground(LeaveGameRequest... params){
			WherewolfPreferences pref = new WherewolfPreferences(GameLobby.this);
			String username = pref.getUsername();
			String password = pref.getPassword();
			int gameid = pref.getCurrentGameID();
			
			
			LeaveGameRequest LeaveGameRequest = new LeaveGameRequest(username, password, gameid);
			return LeaveGameRequest.execute(new WherewolfNetworking());
		}
		
		@Override
		protected void onPostExecute(LeaveGameResponse params){
			
			final TextView errorText = (TextView) findViewById(R.id.error_text);

			
			if (params.getStatus().equals("success"))
			{
		
				
				Context context = getApplicationContext();
				CharSequence text = "You have left the game.";
				int duration = Toast.LENGTH_LONG;

				Toast toast = Toast.makeText(context, text, duration);
				startGameSelection();
				toast.show();

			}else{
				
				errorText.setText(params.getErrorMessage());	
		}
	}
	}
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_game_lobby);
		
		final Button button = (Button) findViewById(R.id.StartGameButton);
		final Button button1 = (Button) findViewById(R.id.LeaveGameButton);
		
		nPlayers = new ArrayList <Players>(); 
		adapter = new LobbyAdapter(this, nPlayers);

		View.OnClickListener main = new View.OnClickListener() {
			public void onClick(View v) {
				startMainScreen();
			
			}
			
		};
		
		View.OnClickListener leave = new View.OnClickListener(){
			public void onClick(View v){
				new LeaveGameTask().execute();
			}
		};
		
		
		button.setOnClickListener(main);
		button1.setOnClickListener(leave);
	}
	
	@Override
	protected void onResume()
	{
		super.onResume();
		new GetPlayerTask().execute();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.game_lobby, menu);
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
