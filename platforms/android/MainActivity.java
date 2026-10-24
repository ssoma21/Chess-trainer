package com.chesstrainer.app;
import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import java.io.InputStream;
public class MainActivity extends Activity {
  private WebView w;
  @Override protected void onCreate(Bundle b) {
    super.onCreate(b);
    w = new WebView(this);
    w.setBackgroundColor(Color.parseColor("#262522"));
    WebSettings s = w.getSettings();
    s.setJavaScriptEnabled(true);
    s.setDomStorageEnabled(true);
    w.setWebViewClient(new WebViewClient() {
      @Override public WebResourceResponse shouldInterceptRequest(WebView v, WebResourceRequest r) {
        if ("appassets.androidplatform.net".equals(r.getUrl().getHost())) {
          try {
            InputStream in = getAssets().open("index.html");
            return new WebResourceResponse("text/html", "utf-8", in);
          } catch (Exception e) { }
        }
        return null;
      }
    });
    setContentView(w);
    w.loadUrl("https://appassets.androidplatform.net/index.html");
  }
  @Override protected void onDestroy() { if (w != null) w.destroy(); super.onDestroy(); }
}
