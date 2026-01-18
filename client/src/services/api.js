const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

export async function fetchGameState() {
  const response = await fetch(`${API_URL}/state`);
  if (!response.ok) {
    throw new Error('Failed to fetch game state');
  }
  return response.json();
}

export async function makeChoice(choiceIndex) {
  const response = await fetch(`${API_URL}/choice`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ choice_index: choiceIndex }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to make choice');
  }
  return response.json();
}

export async function allocateStat(statName) {
  const response = await fetch(`${API_URL}/allocate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ stat_name: statName }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to allocate stat');
  }
  return response.json();
}

export async function resetGame() {
  const response = await fetch(`${API_URL}/reset`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ confirm: true }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to reset game');
  }
  return response.json();
}

export async function sendCombatAction(action) {
  const response = await fetch(`${API_URL}/combat/action`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action }),
  });
  
  if (!response.ok) {
     const error = await response.json();
     throw new Error(error.detail || 'Failed to perform action');
  }
  return response.json();
}

export async function debugStartCombat() {
  const response = await fetch(`${API_URL}/debug/combat`, {
    method: 'POST',
  });
  if (!response.ok) return;
  return response.json();
}

export async function equipItem(itemIndex) {
  const response = await fetch(`${API_URL}/equip`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ item_index: itemIndex }),
  });
  
  if (!response.ok) {
     const error = await response.json();
     throw new Error(error.detail || 'Failed to equip item');
  }
  return response.json();
}
