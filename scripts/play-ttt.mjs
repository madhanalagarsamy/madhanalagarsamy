// scripts/play-ttt.mjs
// Handles Community-Playable Tic-Tac-Toe via GitHub Issues
import fs from "node:fs/promises";

const issueTitle = (process.env.ISSUE_TITLE || process.argv[2] || "").trim();
const issueUser = (process.env.ISSUE_USER || process.argv[3] || "Player").trim();
const issueNumber = (process.env.ISSUE_NUMBER || process.argv[4] || "").trim();
const repoOwner = process.env.GH_USERNAME || process.env.GITHUB_REPOSITORY_OWNER || "madhanalagarsamy";
const repoFull = process.env.GITHUB_REPOSITORY || `${repoOwner}/madhanalagarsamy`;
const [owner, repo] = repoFull.split("/");
const token = process.env.GH_TOKEN || process.env.GITHUB_TOKEN;

const DATA_FILE = "data/tic-tac-toe.json";
const README_FILE = "README.md";

const WIN_COMBOS = [
  [[0,0],[0,1],[0,2]],
  [[1,0],[1,1],[1,2]],
  [[2,0],[2,1],[2,2]],
  [[0,0],[1,0],[2,0]],
  [[0,1],[1,1],[2,1]],
  [[0,2],[1,2],[2,2]],
  [[0,0],[1,1],[2,2]],
  [[0,2],[1,1],[2,0]],
];

function checkWinner(board, player) {
  return WIN_COMBOS.some(combo => combo.every(([r, c]) => board[r][c] === player));
}

function isBoardFull(board) {
  return board.every(row => row.every(cell => cell !== " "));
}

function getAvailableMoves(board) {
  const moves = [];
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 3; c++) {
      if (board[r][c] === " ") moves.push([r, c]);
    }
  }
  return moves;
}

// Smart AI for Bot ('O')
function findBestMove(board) {
  const available = getAvailableMoves(board);
  if (available.length === 0) return null;

  // 1. Can Bot win right now?
  for (const [r, c] of available) {
    board[r][c] = "O";
    if (checkWinner(board, "O")) {
      board[r][c] = " ";
      return [r, c];
    }
    board[r][c] = " ";
  }

  // 2. Can User win next move? Block them!
  for (const [r, c] of available) {
    board[r][c] = "X";
    if (checkWinner(board, "X")) {
      board[r][c] = " ";
      return [r, c];
    }
    board[r][c] = " ";
  }

  // 3. Take center if available
  if (board[1][1] === " ") return [1, 1];

  // 4. Take corners if available
  const corners = [[0,0],[0,2],[2,0],[2,2]].filter(([r, c]) => board[r][c] === " ");
  if (corners.length > 0) {
    return corners[Math.floor(Math.random() * corners.length)];
  }

  // 5. Pick random available move
  return available[Math.floor(Math.random() * available.length)];
}

function renderBoardMarkdown(state) {
  const rawBase = `https://raw.githubusercontent.com/${owner}/${repo}/main/assets/ttt`;
  const issueBase = `https://github.com/${owner}/${repo}/issues/new`;
  const newGameUrl = `${issueBase}?title=ttt%7Cnew&body=Click+%27Submit+new+issue%27+to+start+a+fresh+game%21`;

  const rowsHtml = state.board.map((row, r) => {
    const colsHtml = row.map((cell, c) => {
      if (cell === "X") {
        return `<img src="${rawBase}/x.svg" width="55" height="55" alt="X" />`;
      }
      if (cell === "O") {
        return `<img src="${rawBase}/o.svg" width="55" height="55" alt="O" />`;
      }
      if (state.status === "in_progress") {
        const moveUrl = `${issueBase}?title=ttt%7Cplay%7C${r}%2C${c}&body=Click+%27Submit+new+issue%27+to+play+at+Row+${r+1}%2C+Column+${c+1}%21`;
        return `<a href="${moveUrl}"><img src="${rawBase}/empty.svg" width="55" height="55" alt="Play Row ${r+1}, Col ${c+1}" /></a>`;
      }
      return `<img src="${rawBase}/empty.svg" width="55" height="55" alt="Empty" />`;
    }).map(td => `    <td align="center" width="65" height="65">${td}</td>`).join("\n");
    return `  <tr>\n${colsHtml}\n  </tr>`;
  }).join("\n");

  let statusText = "";
  if (state.status === "user_won") {
    statusText = `🎉 **Game Over!** You won! Congrats @${state.lastPlayer}! [Click here to Play Again](${newGameUrl})`;
  } else if (state.status === "bot_won") {
    statusText = `🤖 **Game Over!** Bot won! [Click here to Rematch](${newGameUrl})`;
  } else if (state.status === "draw") {
    statusText = `🤝 **Game Over!** It's a draw! [Click here to Play Again](${newGameUrl})`;
  } else {
    const last = state.lastPlayer ? `Last move played by **@${state.lastPlayer}**` : `Game in progress!`;
    statusText = `🎮 **Your turn (X)!** Click any empty square above to make a move. &bull; ${last}`;
  }

  const stats = state.stats || { communityWins: 0, botWins: 0, draws: 0, totalGames: 0 };
  const statsText = `🏆 **Community:** ${stats.communityWins} wins &bull; 🤖 **Bot:** ${stats.botWins} wins &bull; 🤝 **Draws:** ${stats.draws} &bull; 🔄 [Start New Game](${newGameUrl})`;

  return `<!-- TTT_START -->
<table align="center">
${rowsHtml}
</table>

<p align="center">
  ${statusText}<br/>
  <sub>${statsText}</sub>
</p>
<!-- TTT_END -->`;
}

async function postCommentAndClose(msg) {
  if (!token || !issueNumber) return;
  const headers = {
    Authorization: `Bearer ${token}`,
    Accept: "application/vnd.github+json",
    "User-Agent": "ttt-action",
  };

  try {
    // Comment
    await fetch(`https://api.github.com/repos/${owner}/${repo}/issues/${issueNumber}/comments`, {
      method: "POST",
      headers,
      body: JSON.stringify({ body: msg }),
    });

    // Close issue
    await fetch(`https://api.github.com/repos/${owner}/${repo}/issues/${issueNumber}`, {
      method: "PATCH",
      headers,
      body: JSON.stringify({ state: "closed" }),
    });
  } catch (err) {
    console.error("Failed to comment or close issue:", err);
  }
}

async function main() {
  let state = {
    board: [
      [" ", " ", " "],
      [" ", " ", " "],
      [" ", " ", " "],
    ],
    status: "in_progress",
    winner: null,
    lastPlayer: null,
    lastMove: null,
    stats: { communityWins: 0, botWins: 0, draws: 0, totalGames: 0 },
  };

  try {
    const raw = await fs.readFile(DATA_FILE, "utf8");
    state = JSON.parse(raw);
  } catch {
    // defaults
  }

  const cmd = issueTitle.toLowerCase();

  let responseMsg = "";

  if (cmd.startsWith("ttt|new") || cmd === "new game") {
    state.board = [
      [" ", " ", " "],
      [" ", " ", " "],
      [" ", " ", " "],
    ];
    state.status = "in_progress";
    state.winner = null;
    state.lastPlayer = issueUser;
    state.lastMove = "New Game Started";
    responseMsg = `🎮 New Tic-Tac-Toe game started by @${issueUser}! Check out the fresh board on the [profile README](https://github.com/${owner}/${repo})!`;
  } else if (cmd.startsWith("ttt|play|")) {
    const parts = cmd.replace("ttt|play|", "").split(",");
    const r = parseInt(parts[0], 10);
    const c = parseInt(parts[1], 10);

    if (isNaN(r) || isNaN(c) || r < 0 || r > 2 || c < 0 || c > 2) {
      responseMsg = `⚠️ Invalid move coordinates \`${parts.join(",")}\`. Must be between 0 and 2.`;
    } else if (state.status !== "in_progress") {
      // Auto-restart game if clicked when game ended
      state.board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "],
      ];
      state.status = "in_progress";
      state.winner = null;
      state.board[r][c] = "X";
      state.lastPlayer = issueUser;
      state.lastMove = `User played [${r+1}, ${c+1}]`;

      const botMove = findBestMove(state.board);
      if (botMove) {
        state.board[botMove[0]][botMove[1]] = "O";
      }

      responseMsg = `🎮 Started a new game with your move at Row ${r+1}, Col ${c+1}!`;
    } else if (state.board[r][c] !== " ") {
      responseMsg = `⚠️ Spot at Row ${r+1}, Col ${c+1} is already taken! Please pick an empty cell on the profile README.`;
    } else {
      // Valid move
      state.board[r][c] = "X";
      state.lastPlayer = issueUser;
      state.lastMove = `User played [${r+1}, ${c+1}]`;

      // Check if User won
      if (checkWinner(state.board, "X")) {
        state.status = "user_won";
        state.winner = "Community (X)";
        state.stats.communityWins = (state.stats.communityWins || 0) + 1;
        state.stats.totalGames = (state.stats.totalGames || 0) + 1;
        responseMsg = `🎉 Amazing move @${issueUser}! You won the game for the community! 🏆`;
      } else if (isBoardFull(state.board)) {
        state.status = "draw";
        state.winner = "Draw";
        state.stats.draws = (state.stats.draws || 0) + 1;
        state.stats.totalGames = (state.stats.totalGames || 0) + 1;
        responseMsg = `🤝 Good game @${issueUser}! It's a draw!`;
      } else {
        // Bot moves
        const botMove = findBestMove(state.board);
        if (botMove) {
          state.board[botMove[0]][botMove[1]] = "O";
          if (checkWinner(state.board, "O")) {
            state.status = "bot_won";
            state.winner = "Bot (O)";
            state.stats.botWins = (state.stats.botWins || 0) + 1;
            state.stats.totalGames = (state.stats.totalGames || 0) + 1;
            responseMsg = `🤖 Bot played at Row ${botMove[0]+1}, Col ${botMove[1]+1} and won! Better luck next time!`;
          } else if (isBoardFull(state.board)) {
            state.status = "draw";
            state.winner = "Draw";
            state.stats.draws = (state.stats.draws || 0) + 1;
            state.stats.totalGames = (state.stats.totalGames || 0) + 1;
            responseMsg = `🤝 Good game @${issueUser}! It ended in a draw!`;
          } else {
            responseMsg = `✅ Your move (Row ${r+1}, Col ${c+1}) was accepted! Bot responded at Row ${botMove[0]+1}, Col ${botMove[1]+1}. It's the community's turn again!`;
          }
        }
      }
    }
  } else {
    responseMsg = `👋 Unrecognized Tic-Tac-Toe command. Visit the [profile README](https://github.com/${owner}/${repo}) to click a square and play!`;
  }

  // Save state
  await fs.mkdir("data", { recursive: true });
  await fs.writeFile(DATA_FILE, JSON.stringify(state, null, 2));

  // Update README
  const tttBlock = renderBoardMarkdown(state);
  let readme = await fs.readFile(README_FILE, "utf8");
  const markerRegex = /<!-- TTT_START -->[\s\S]*?<!-- TTT_END -->/;
  if (markerRegex.test(readme)) {
    readme = readme.replace(markerRegex, tttBlock);
  } else {
    // Insert before social badges
    const socialMarker = "<!-- ===== SOCIAL BADGES ===== -->";
    if (readme.includes(socialMarker)) {
      readme = readme.replace(socialMarker, `<!-- ===== COMMUNITY GAME ===== -->\n\n<div align="center">\n\n### 🕹️ Community Playable Tic-Tac-Toe\n\n${tttBlock}\n\n</div>\n\n<!-- ===== END COMMUNITY GAME ===== -->\n<br/>\n\n${socialMarker}`);
    } else {
      readme += `\n\n${tttBlock}\n`;
    }
  }

  await fs.writeFile(README_FILE, readme);
  console.log("Updated Tic-Tac-Toe game state & README.md successfully.");

  // Post comment & close issue
  if (responseMsg) {
    await postCommentAndClose(responseMsg);
  }
}

main().catch(err => {
  console.error("Error running play-ttt.mjs:", err);
  process.exit(1);
});
