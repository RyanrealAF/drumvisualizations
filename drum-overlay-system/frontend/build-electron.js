const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('Building Electron application...');

try {
  // Build the React application
  console.log('Building React frontend...');
  execSync('npm run build', { stdio: 'inherit', cwd: __dirname });
  
  // Build the Electron application
  console.log('Building Electron executable...');
  execSync('npx electron-builder', { stdio: 'inherit', cwd: __dirname });
  
  console.log('Build completed successfully!');
  console.log('Executable files are in the dist/ directory');
} catch (error) {
  console.error('Build failed:', error.message);
  process.exit(1);
}