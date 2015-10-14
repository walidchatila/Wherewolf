package edu.utexas.chatila.wherewolf;

import android.content.Context;
import android.content.SharedPreferences;

public class WherewolfPreferences {

  private static final String PREF_URI = "edu.utexas.werewolf.prefs";
  
  Context context;
  private SharedPreferences sharedPreferences;
  
  public WherewolfPreferences(Context context)
  {
      this.context = context;
      sharedPreferences = context
              .getSharedPreferences(PREF_URI,
                      Context.MODE_PRIVATE);
      
  }
  
  public String getUsername()
  {
      return sharedPreferences.getString("username", "");
  }
  
  public String getPassword()
  {
      return sharedPreferences.getString("password", "");
  }
  
  public int getCurrentGameID()
  {
      return sharedPreferences.getInt("currentGame", 0);
  }
  
  public void setCreds(String username, String password)
  {
      SharedPreferences.Editor editor = sharedPreferences.edit();
      
      editor.putString("username", username);
      editor.putString("password", password);
      editor.commit();
  }
  
  public void setCurrentGameID(int gameID)
  {
      SharedPreferences.Editor editor = sharedPreferences.edit();
      editor.putInt("currentGame", gameID);
      editor.commit();
  }
  
}