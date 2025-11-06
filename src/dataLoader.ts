/**
 * Data Loader Module
 *
 * Provides functions to load and validate Event and Attendee data from JSON files.
 * Uses TypeScript type guards for runtime validation.
 */

import { readFile, readdir } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import type { Event, Attendee } from './types/index.js';
import { isEvent, isAttendee } from './types/index.js';

// Get directory name for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Base paths for data directories
const DATA_DIR = join(__dirname, '..', 'data');
const EVENTS_DIR = join(DATA_DIR, 'events');
const ATTENDEES_DIR = join(DATA_DIR, 'attendees');

/**
 * Loads and validates event data from JSON file
 *
 * @param eventId - The event identifier (e.g., "event-2025")
 * @returns Promise resolving to validated Event object
 * @throws Error if file not found or data is invalid
 */
export async function loadEvent(eventId: string): Promise<Event> {
  try {
    const filePath = join(EVENTS_DIR, `${eventId}.json`);
    const fileContent = await readFile(filePath, 'utf-8');
    const data = JSON.parse(fileContent);

    if (!isEvent(data)) {
      throw new Error(`Invalid event data structure in ${filePath}`);
    }

    return data;
  } catch (error) {
    if (error instanceof Error) {
      if ('code' in error && error.code === 'ENOENT') {
        throw new Error(`Event file not found: ${eventId}`);
      }
      throw error;
    }
    throw new Error(`Failed to load event: ${eventId}`);
  }
}

/**
 * Loads and validates attendee data from JSON file
 *
 * @param attendeeId - The attendee identifier (e.g., "1001")
 * @returns Promise resolving to validated Attendee object
 * @throws Error if file not found or data is invalid
 */
export async function loadAttendee(attendeeId: string): Promise<Attendee> {
  try {
    const filePath = join(ATTENDEES_DIR, `${attendeeId}.json`);
    const fileContent = await readFile(filePath, 'utf-8');
    const data = JSON.parse(fileContent);

    if (!isAttendee(data)) {
      throw new Error(`Invalid attendee data structure in ${filePath}`);
    }

    return data;
  } catch (error) {
    if (error instanceof Error) {
      if ('code' in error && error.code === 'ENOENT') {
        throw new Error(`Attendee file not found: ${attendeeId}`);
      }
      throw error;
    }
    throw new Error(`Failed to load attendee: ${attendeeId}`);
  }
}

/**
 * Loads all attendee data files from the attendees directory
 *
 * @returns Promise resolving to array of validated Attendee objects
 * @throws Error if directory cannot be read or any file is invalid
 */
export async function loadAllAttendees(): Promise<Attendee[]> {
  try {
    const files = await readdir(ATTENDEES_DIR);
    const jsonFiles = files.filter(file => file.endsWith('.json'));

    if (jsonFiles.length === 0) {
      return [];
    }

    // Load all attendees in parallel
    const attendeePromises = jsonFiles.map(file => {
      const attendeeId = file.replace('.json', '');
      return loadAttendee(attendeeId);
    });

    const attendees = await Promise.all(attendeePromises);

    return attendees;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Failed to load attendees');
  }
}

/**
 * Gets a list of all available attendee IDs
 *
 * @returns Promise resolving to array of attendee ID strings
 */
export async function getAttendeeIds(): Promise<string[]> {
  try {
    const files = await readdir(ATTENDEES_DIR);
    return files
      .filter(file => file.endsWith('.json'))
      .map(file => file.replace('.json', ''));
  } catch (error) {
    throw new Error('Failed to read attendee directory');
  }
}

/**
 * Checks if an attendee exists
 *
 * @param attendeeId - The attendee identifier to check
 * @returns Promise resolving to boolean indicating existence
 */
export async function attendeeExists(attendeeId: string): Promise<boolean> {
  try {
    await loadAttendee(attendeeId);
    return true;
  } catch {
    return false;
  }
}
