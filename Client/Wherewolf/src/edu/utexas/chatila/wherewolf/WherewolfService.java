package edu.utexas.chatila.wherewolf;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Process;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.IBinder;
import android.os.Looper;
import android.os.PowerManager;
import android.os.PowerManager.WakeLock;
import android.util.Log;
import android.widget.Toast;

public class WherewolfService extends Service implements LocationListener {
	
	private static final String TAG = "WherewolfService";
	  // number of milliseconds before a location update
	  private static final int REPORT_PERIOD = 5000;
	  private static final int MIN_CHANGE = 0;
	  // allows us to prevent the CPU from going to sleep.
	  private WakeLock wakeLock;
	  // allows us to register updates to the GPS system
	  private LocationManager locationManager;
	  private boolean isNight = false;
	  private Games currentGame = null;
	  private Players currentPlayer = null;
	  private Looper mServiceLooper;
	  private Handler handler;
	  
	  private String username;
	  private String password;
	  private int gameID;
	  private String cl;
	  
	  // more methods will go here	  	
	 private class ChangedLocationTask extends AsyncTask<Void, Integer, ChangedLocationResponse> {
	      @Override
	      protected ChangedLocationResponse doInBackground(Void... request) {
	          // final EditText nameTV = (EditText) findViewById(R.id.usernameText);
	          // final EditText passTV = (EditText) findViewById(R.id.passwordText);
	    	  WherewolfPreferences pref = new WherewolfPreferences(WherewolfService.this);
	    	  username = pref.getUsername();
	    	  password = pref.getPassword();
	    	  gameID = pref.getCurrentGameID();
	    	  ChangedLocationRequest cLrequest = new ChangedLocationRequest(username, password,gameID);
	    	  return cLrequest.execute(new WherewolfNetworking());
				/*
	            ChangedLocationRequest cLrequest = new ChangedLocationRequest(locMsg, locMsg, 0);
				return cLrequest.execute(new WherewolfNetworking());
	            Toast.makeText(getApplicationContext(), locMsg, Toast.LENGTH_SHORT).show();   */
		      }
	      
	      protected void onPostExecute(ChangedLocationResponse result) {
	          Log.v(TAG, "Changed location for user in game id " + result.getGameID());
	          /* result.geterrormessage - dump this response to this text field*/
	          cl = "updated location";
	          if (result.getStatus().equals("success")) {
		    	  WherewolfPreferences pref = new WherewolfPreferences(WherewolfService.this);
		    	  username = pref.getUsername();
		    	  password = pref.getPassword();
		    	  gameID = pref.getCurrentGameID();
	              Log.v(TAG, "Changing Location");
	              
	              Toast.makeText(getApplicationContext(), cl, Toast.LENGTH_SHORT).show(); 
	          } else {
	              // do something with bad password
	              //errorText.setText(result.getErrorMessage());
	          }
	      }
		}
		      
	  
	  public void setNight()
	  {
	    handler.post( new Runnable() {
	        @Override
	        public void run ()
	        {
	            wakeLock.acquire();
	            // makes location updates happen every 5 seconds, with no minimum 
	            // distance for change notification            
	            locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER,
	                REPORT_PERIOD, MIN_CHANGE, WherewolfService.this);
	            isNight = true;
	        }
	        });
	  }
	  public void setDay() {
	        handler.post(new Runnable() {
	            @Override
	            public void run() {
	                // Log.i(TAG, "Setting to day, turning off tracking");
	                if (isNight) {
	                    if (wakeLock.isHeld()) {
	                        wakeLock.release();
	                    }
	                    locationManager.removeUpdates(WherewolfService.this);
	                    isNight = false;
	                    Log.i(TAG, "Setting to day, turning off tracking");
	                    
	                }
	            }
	        });
	    }
	  
	  @Override
	  public void onCreate() {
	    super.onCreate();
	    HandlerThread thread = new HandlerThread("WherewolfThread",
	        Process.THREAD_PRIORITY_BACKGROUND);
	    thread.start();
	    mServiceLooper = thread.getLooper();
	    handler = new Handler(mServiceLooper);
	    locationManager = (LocationManager) getApplicationContext()
	                .getSystemService(Context.LOCATION_SERVICE);
	    PowerManager pm = (PowerManager) getSystemService(POWER_SERVICE);
	    wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "DoNotSleep");
	    setNight();
	  }
	  
	  @Override
	  public int onStartCommand(Intent intent, int flags, int startId)
	  {
	    return START_STICKY;
	  }
	  public IBinder onBind(Intent intent) {
	    return null;
	  }
	  @Override
	  public void onDestroy() {
	    locationManager.removeUpdates(this);
	  }
	  
	  private void showLocation(String msg){
		  Toast.makeText(this, msg, Toast.LENGTH_SHORT).show();
	  }
	  	  
	
	@Override
	public void onLocationChanged(Location location) {
		// TODO Auto-generated method stub
	      if (location != null) {
	            final String locMsg = "location changed "
	                    + location.getLatitude() + " "
	                    + location.getLongitude();
	            Toast.makeText(getApplicationContext(), locMsg, Toast.LENGTH_SHORT).show();
	            showLocation(locMsg);
	            Log.i(TAG, locMsg);
	            new ChangedLocationTask().execute();
	            
	            // ChangedLocationRequest request = new ChangedLocationRequest(locMsg, locMsg, 0);
	            // Toast.makeText(getApplicationContext(), locMsg, Toast.LENGTH_SHORT).show();
	            
	            // WherewolfNetworking net = new WherewolfNetworking();
	            
	            // net.sendServerUpdate();
	            
	            // net.sendServerUpdate();
	            // Log.i(TAG, "Network is " + net.isNetworkAvailable(getApplicationContext()));
	            // Message msg = mServiceHandler.obtainMessage();
	            // msg.arg1 = ++counter;
	            // mServiceHandler.sendMessage(msg);
	        }
	  }
	@Override
	public void onStatusChanged(String provider, int status, Bundle extras) {
		// TODO Auto-generated method stub
		
	}
	@Override
	public void onProviderEnabled(String provider) {
		// TODO Auto-generated method stub
		
	}
	@Override
	public void onProviderDisabled(String provider) {
		// TODO Auto-generated method stub
		
	};
}