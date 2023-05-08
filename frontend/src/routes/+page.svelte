<script>
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';

  // Initialising variables
  let playerOneScore = 0;
  let playerTwoScore = 0;
  let winner = '';
  let lastPlayer = null;
  const dispatch = createEventDispatcher();

  // Function to add a point to a player
  async function addPoint(player) {
  try {
    // Send a request to the server to update the score
    const response = await fetch("http://localhost:5000/update_score", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ player }),
    });
    const data = await response.json();

    // Update based on request
    if (data.success) {
      if (data.player === 1) {
        playerOneScore += 1;
      } else if (data.player === 2) {
        playerTwoScore += 1;
      }
      lastPlayer = data.player;
    }
  } catch (error) {
    console.error("Error updating score:", error);
  }
}

// Function to delete the previous point
async function deletePreviousPoint() {
    if (lastPlayer) {
      try {
        // Send a request to the server to delete the previous point
        const response = await fetch("http://localhost:5000/delete_previous_point", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}),
        });

        const data = await response.json();

        // Update based on request
        if (data.success) {
          if (data.player === 1 && playerOneScore > 0) {
            playerOneScore -= 1;
          } else if (data.player === 2 && playerTwoScore > 0) {
            playerTwoScore -= 1;
          }
          lastPlayer = null;
        }
      } catch (error) {
        console.error("Error deleting previous point:", error);
      }
    }
  }

  // Check for a winner 
  $: winner = playerOneScore >= 21 ? 'Player 1' : playerTwoScore >= 21 ? 'Player 2' : '';

  // Function to reset the game
  function resetGame() {
    playerOneScore = 0;
    playerTwoScore = 0;
    winner = '';
  }

  // Show the modal when there is a winner
  onMount(() => {
    if (winner) {
      dispatch('show-modal');
    }
  });
</script>

<!-- Main content -->
<main>
  <h1>Badminton Score</h1>

  <!-- svelte-ignore a11y-img-redundant-alt -->
  <img style="margin-bottom: 1rem;" src="/badminton_racket.jpg" alt="Badminton Image" width="450" height="450">
  
  <div class="inputs">
    <!-- Input forms for player names -->
    <form style="margin-right: 2rem;">
      <label for="fname">Player 1 Name:</label><br>
      <input type="text" id="p1name" name="p1name"><br>
    </form>

    <form>
      <label for="fname">Player 2 Name:</label><br>
      <input type="text" id="p2name" name="p2name"><br>
    </form>
  </div>

  <!-- Display scores and buttons to add points for each player -->
  <div class="scoreboard">
    <div class="player player-one">
      <button style="margin-left: 2.5rem;" on:click={() => addPoint(1)}>+</button>
      <p style="margin-left: 2.5rem;">{playerOneScore}</p>
    </div>

    <div class="player player-two">
      <button style="margin-right: 2.5rem;" on:click={() => addPoint(2)}>+</button>
      <p style="margin-right: 2.5rem;" >{playerTwoScore}</p>
    </div>
  </div>

  <!-- Button to delete the previous point -->
  <button style="margin-bottom: 2rem;" on:click={() => deletePreviousPoint()}>Delete previous point</button>
  
  <!-- Display the winner and a button to reset the game when there is a winner -->
  {#if winner}
  <div
  class="modal-overlay"
  on:click={() => resetGame()}
  on:keydown={(event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      resetGame();
    }
  }}
  tabindex="0" 
  role="button" 
  aria-label="Reset game"
>

      <div class="modal">
        <h2>{winner} wins!</h2>
        <button on:click={() => resetGame()}>Reset</button>
      </div>
    </div>
  {/if}
</main>

<!-- Import the styles -->
<style>
  @import './scoreboard.css';
</style>