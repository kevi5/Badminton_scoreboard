<script>
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';

  let playerOneScore = 0;
  let playerTwoScore = 0;
  let winner = '';
  let lastPlayer = null;
  const dispatch = createEventDispatcher();

  async function addPoint(player) {
  try {
    const response = await fetch("http://localhost:5000/update_score", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ player }),
    });
    const data = await response.json();

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
async function deletePreviousPoint() {
    if (lastPlayer) {
      try {
        const response = await fetch("http://localhost:5000/delete_previous_point", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}),
        });

        const data = await response.json();

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

  $: winner = playerOneScore >= 21 ? 'Player 1' : playerTwoScore >= 21 ? 'Player 2' : '';

  function resetGame() {
    playerOneScore = 0;
    playerTwoScore = 0;
    winner = '';
  }

  onMount(() => {
    if (winner) {
      dispatch('show-modal');
    }
  });
</script>

<main>
  <h1>Badminton Score</h1>
  <!-- svelte-ignore a11y-img-redundant-alt -->
  <img style="margin-bottom: 1rem;" src="/badminton_racket.jpg" alt="Badminton Image" width="450" height="450">
  <div class="inputs">
    <form style="margin-right: 2rem;">
      <label for="fname">Player 1 Name:</label><br>
      <input type="text" id="p1name" name="p1name"><br>
    </form>
    <form>
      <label for="fname">Player 2 Name:</label><br>
      <input type="text" id="p2name" name="p2name"><br>
    </form>
  </div>
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
  <button style="margin-bottom: 2rem;" on:click={() => deletePreviousPoint()}>Delete previous point</button>
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

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: beige;
  }

  .scoreboard {
    display: flex;
    justify-content: space-between;
    width: 300px;
    align-items: center;
  }

  .inputs {
    display: flex;
    margin-bottom: 2rem;
    font-weight: bold;
  }

  .player {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .player p {
    font-size: 2rem;
  }

  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    background-color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
</style>