using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class ScriptLogic : MonoBehaviour
{
    public int playerScore;
    public Text scoretext;

    [ContextMenu("Increase Score")]
    public void addScore()
    {
        playerScore = playerScore + 1;
        scoretext.text = playerScore.ToString();
    }
}
