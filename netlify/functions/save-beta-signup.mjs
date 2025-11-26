/**
 * SAVE BETA SIGNUP
 * Netlify serverless function to save Araya beta signup data
 * Stores signup information before Stripe checkout
 */

import { writeFile, readFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import path from 'path';

export async function handler(event, context) {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: ''
    };
  }

  try {
    // Parse request body
    const signupData = JSON.parse(event.body);

    // Validate required fields
    if (!signupData.email || !signupData.name) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
          error: 'Missing required fields: email and name'
        })
      };
    }

    // Add timestamp and ID
    const signup = {
      id: Date.now() + '-' + Math.random().toString(36).substring(7),
      ...signupData,
      timestamp: new Date().toISOString(),
      status: 'pending_payment'
    };

    // Define data directory
    const dataDir = path.join(process.cwd(), '.data');
    const signupsFile = path.join(dataDir, 'beta-signups.json');

    // Ensure data directory exists
    if (!existsSync(dataDir)) {
      await mkdir(dataDir, { recursive: true });
    }

    // Read existing signups or initialize empty array
    let signups = [];
    if (existsSync(signupsFile)) {
      const fileContent = await readFile(signupsFile, 'utf-8');
      signups = JSON.parse(fileContent);
    }

    // Add new signup
    signups.push(signup);

    // Write back to file
    await writeFile(signupsFile, JSON.stringify(signups, null, 2));

    console.log('Beta signup saved:', {
      id: signup.id,
      email: signup.email,
      name: signup.name,
      useCase: signup.useCase || 'not specified'
    });

    // Return success response
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: true,
        signupId: signup.id,
        message: 'Signup saved successfully'
      })
    };

  } catch (error) {
    console.error('Error saving signup:', error);

    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        error: 'Failed to save signup',
        details: error.message
      })
    };
  }
}
