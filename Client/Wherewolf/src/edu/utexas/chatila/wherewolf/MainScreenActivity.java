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
import android.widget.ListView;
import android.widget.SeekBar;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.Toast;


public class MainScreenActivity extends Activity {
	
	private static final String TAG = "Main";

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
	
private class GetPlayerTask extends AsyncTask<GetPlayerRequest, Integer, GetPlayerResponse>{
		
		@Override
		protected GetPlayerResponse doInBackground(GetPlayerRequest... params){
			WherewolfPreferences pref = new WherewolfPreferences(MainScreenActivity.this);
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
			
			ListView gameListView = (ListView) findViewById(R.id.player_main_list);
			gameListView.setAdapter(adapter);
			
			gameListView.setOnItemClickListener(new OnItemClickListener(){
			      public void onItemClick(      AdapterView<?> parent,      View v,      int position,      long id){
			    	  Context context = getApplicationContext();
			    	  CharSequence text = "You have casted a vote!";
			    	  int duration = Toast.LENGTH_LONG;


			    	  Toast.makeText(context, text, duration).show();
			    	 
			      }
			}
			);
			
			      }
			}
		

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main_screen);
		
		nPlayers = new ArrayList <Players>(); 
		adapter = new LobbyAdapter(this, nPlayers);

	
		final CircadianWidgetView circadianWidget = (CircadianWidgetView) findViewById(R.id.circadian);
		final SeekBar seekbar = (SeekBar) findViewById(R.id.daytime_seekbar);
		MyOnChangeListener changeListener = new MyOnChangeListener();
		changeListener.setCircadianWidget(circadianWidget);
		seekbar.setOnSeekBarChangeListener(changeListener);
		
		
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
		getMenuInflater().inflate(R.menu.main_screen, menu);
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


