/**
 * Type definitions for Personal Event Summary system
 *
 * These types define the structure of mock data used to generate
 * personalized attendee summary pages.
 */

/**
 * Represents a call-to-action button or link
 */
export interface CallToAction {
  /** Display text for the CTA */
  text: string;
  /** URL the CTA links to */
  url: string;
  /** Type of CTA (primary, secondary, etc.) */
  type: 'primary' | 'secondary' | 'tertiary';
  /** Optional tracking parameter */
  trackingId?: string;
}

/**
 * Represents a product explored by an attendee at a B2B event
 */
export interface Product {
  /** Product name */
  name: string;
  /** Company offering the product */
  company: string;
  /** Product category */
  category: string;
}

/**
 * Represents a booth visit at a B2B event
 */
export interface BoothVisit {
  /** Company name */
  company: string;
  /** Time spent at booth in minutes */
  timeSpentMinutes: number;
  /** Products viewed at the booth */
  productsViewed: string[];
}

/**
 * Represents an interaction with an event sponsor
 */
export interface SponsorInteraction {
  /** Sponsor name */
  sponsor: string;
  /** Type of interaction */
  type: 'booth_visit' | 'demo_request' | 'meeting' | 'download' | 'other';
  /** Timestamp of interaction */
  timestamp: string;
}

/**
 * Represents a session at an event
 */
export interface Session {
  /** Unique session identifier */
  id: string;
  /** Session title */
  title: string;
  /** Session description */
  description: string;
  /** Speaker name(s) */
  speakers: string[];
  /** Session date and time */
  dateTime: string;
  /** Session duration in minutes */
  durationMinutes: number;
  /** Session track or category */
  track?: string;
}

/**
 * Represents a connection made at an event
 */
export interface Connection {
  /** Name of the connection */
  name: string;
  /** Job title */
  title: string;
  /** Company name */
  company: string;
  /** LinkedIn profile URL (optional) */
  linkedIn?: string;
}

/**
 * Represents attendee statistics and highlights
 */
export interface AttendeeStats {
  /** Total number of sessions attended */
  sessionsAttended: number;
  /** Total number of connections made */
  connectionsMade: number;
  /** Hours spent at the event */
  hoursAttended: number;
  /** Number of different tracks explored */
  tracksExplored: number;
  /** Key achievement or highlight */
  topAchievement?: string;
}

/**
 * Represents an event
 */
export interface Event {
  /** Unique event identifier */
  id: string;
  /** Event name */
  name: string;
  /** Event description */
  description: string;
  /** Event location (city, venue) */
  location: string;
  /** Event start date */
  startDate: string;
  /** Event end date */
  endDate: string;
  /** Total number of attendees */
  totalAttendees: number;
  /** Total number of sessions offered */
  totalSessions: number;
  /** Event website URL */
  websiteUrl: string;
  /** Event logo URL (relative path) */
  logoUrl?: string;
}

/**
 * Represents an event attendee with personalized data
 */
export interface Attendee {
  /** Unique attendee identifier */
  id: string;
  /** Attendee first name */
  firstName: string;
  /** Attendee last name */
  lastName: string;
  /** Attendee email */
  email: string;
  /** Company name */
  company: string;
  /** Job title */
  title: string;
  /** Event ID this attendee participated in */
  eventId: string;
  /** Sessions this attendee participated in */
  sessions: Session[];
  /** Connections made at the event */
  connections: Connection[];
  /** Personalized statistics and highlights */
  stats: AttendeeStats;
  /** Call-to-action items for re-engagement */
  callsToAction: CallToAction[];
  /** Registration date */
  registeredAt: string;
  /** Products explored at B2B event (optional) */
  productsExplored?: Product[];
  /** Booths visited at B2B event (optional) */
  boothsVisited?: BoothVisit[];
  /** Sponsor interactions at B2B event (optional) */
  sponsorInteractions?: SponsorInteraction[];
}

/**
 * Type guard to check if an object is a valid Event
 */
export function isEvent(obj: unknown): obj is Event {
  if (typeof obj !== 'object' || obj === null) return false;
  const e = obj as Event;
  return (
    typeof e.id === 'string' &&
    typeof e.name === 'string' &&
    typeof e.description === 'string' &&
    typeof e.location === 'string' &&
    typeof e.startDate === 'string' &&
    typeof e.endDate === 'string' &&
    typeof e.totalAttendees === 'number' &&
    typeof e.totalSessions === 'number' &&
    typeof e.websiteUrl === 'string'
  );
}

/**
 * Type guard to check if an object is a valid Session
 */
export function isSession(obj: unknown): obj is Session {
  if (typeof obj !== 'object' || obj === null) return false;
  const s = obj as Session;
  return (
    typeof s.id === 'string' &&
    typeof s.title === 'string' &&
    typeof s.description === 'string' &&
    Array.isArray(s.speakers) &&
    s.speakers.every(sp => typeof sp === 'string') &&
    typeof s.dateTime === 'string' &&
    typeof s.durationMinutes === 'number'
  );
}

/**
 * Type guard to check if an object is a valid Attendee
 */
export function isAttendee(obj: unknown): obj is Attendee {
  if (typeof obj !== 'object' || obj === null) return false;
  const a = obj as Attendee;

  // Check required fields
  const hasRequiredFields = (
    typeof a.id === 'string' &&
    typeof a.firstName === 'string' &&
    typeof a.lastName === 'string' &&
    typeof a.email === 'string' &&
    typeof a.company === 'string' &&
    typeof a.title === 'string' &&
    typeof a.eventId === 'string' &&
    Array.isArray(a.sessions) &&
    Array.isArray(a.connections) &&
    Array.isArray(a.callsToAction) &&
    typeof a.stats === 'object' &&
    typeof a.registeredAt === 'string'
  );

  if (!hasRequiredFields) return false;

  // Validate optional B2B fields if present
  if (a.productsExplored !== undefined && !Array.isArray(a.productsExplored)) {
    return false;
  }

  if (a.boothsVisited !== undefined && !Array.isArray(a.boothsVisited)) {
    return false;
  }

  if (a.sponsorInteractions !== undefined && !Array.isArray(a.sponsorInteractions)) {
    return false;
  }

  return true;
}

/**
 * Type guard to check if an object is a valid CallToAction
 */
export function isCallToAction(obj: unknown): obj is CallToAction {
  if (typeof obj !== 'object' || obj === null) return false;
  const cta = obj as CallToAction;
  return (
    typeof cta.text === 'string' &&
    typeof cta.url === 'string' &&
    (cta.type === 'primary' || cta.type === 'secondary' || cta.type === 'tertiary')
  );
}
