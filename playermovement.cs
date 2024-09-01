using System.Collections;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    private float horizontal;
    private float speed = 8f;
    private float jumpingPower = 16f;
    private bool isFacingRight = true;
    private Collider2D _collider;
    private Vector2 _respawnPoint;


    [SerializeField] private bool _active = true; 
    [SerializeField] private Rigidbody2D rb;
    [SerializeField] private Transform groundCheck;
    [SerializeField] private LayerMask groundLayer;

    private void Start()
    {
        _collider = GetComponent<Collider2D>();
        SetRespawnPoint (transform.position);
    }
    void Update()
    {

        if (!_active)
        {
            return;
        }

        horizontal = Input.GetAxisRaw("Horizontal");

        if (Input.GetButtonDown("Jump") && IsGrounded())
        {
            rb.velocity = new Vector2(rb.velocity.x, jumpingPower);
        }

        if (Input.GetButtonUp("Jump") && rb.velocity.y > 0f)
        {
            rb.velocity = new Vector2(rb.velocity.x, rb.velocity.y * 0.5f);
        }

        Flip();
    }

    private void FixedUpdate()
    {
        rb.velocity = new Vector2(horizontal * speed, rb.velocity.y);
    }

    private bool IsGrounded()
    {
        return Physics2D.OverlapCircle(groundCheck.position, 0.2f, groundLayer);
    }

    private void Flip()
    {
        if (isFacingRight && horizontal < 0f || !isFacingRight && horizontal > 0f)
        {
            isFacingRight = !isFacingRight;
            Vector3 localScale = transform.localScale;
            localScale.x *= -1f;
            transform.localScale = localScale;
        }
    }

    private void MiniJump()
    {
        rb.velocity = new Vector2(rb.velocity.x, jumpingPower);
    }

    public void SetRespawnPoint(Vector2 position)
    {
        _respawnPoint = position;
    }
    public void Die()
    {
        _active = false;
        _collider.enabled = false;
        MiniJump();
        StartCoroutine(Respawn());
        
    }

    private IEnumerator Respawn()
    {
        yield return new WaitForSeconds(1f);
        transform.position = _respawnPoint;
        _active = true;
        _collider.enabled = true;
        MiniJump() ;    

    }

}