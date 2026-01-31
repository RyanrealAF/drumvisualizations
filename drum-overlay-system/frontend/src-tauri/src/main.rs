#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

use tauri::{Manager, WindowBuilder, WindowUrl};

#[derive(Clone, serde::Serialize)]
struct Payload {
  args: Vec<String>,
  cwd: String,
}

#[tauri::command]
async fn open_overlay_window(window: tauri::Window) -> Result<(), String> {
  let overlay_window = WindowBuilder::new(
    &window.app_handle(),
    "overlay",
    WindowUrl::App("overlay.html".into()),
  )
  .title("Drum Overlay")
  .resizable(false)
  .decorations(false)
  .always_on_top(true)
  .skip_taskbar(true)
  .build()
  .map_err(|e| e.to_string())?;

  // Center the overlay window
  if let Some(primary_monitor) = overlay_window.primary_monitor().await {
    if let Some(monitor_size) = primary_monitor.size().to_logical::<f64>(overlay_window.scale_factor().await.unwrap_or(1.0)) {
      let x = (monitor_size.width - 1920.0) / 2.0;
      let y = (monitor_size.height - 1080.0) / 2.0;
      overlay_window.set_position(tauri::Position::XY(x, y)).await.map_err(|e| e.to_string())?;
    }
  }

  Ok(())
}

#[tauri::command]
async fn close_overlay_window(window: tauri::Window) -> Result<(), String> {
  if let Some(overlay_window) = window.get_window("overlay") {
    overlay_window.close().map_err(|e| e.to_string())?;
  }
  Ok(())
}

fn main() {
  tauri::Builder::default()
    .setup(|app| {
      #[cfg(debug_assertions)]
      {
        let window = app.get_window("main").unwrap();
        window.open_devtools();
      }
      Ok(())
    })
    .on_window_event(|event| match event.event() {
      tauri::WindowEvent::CloseRequested { .. } => {
        std::process::exit(0);
      }
      _ => {}
    })
    .invoke_handler(tauri::generate_handler![open_overlay_window, close_overlay_window])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
