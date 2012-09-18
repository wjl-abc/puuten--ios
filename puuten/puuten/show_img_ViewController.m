//
//  show_img_ViewController.m
//  puuten
//
//  Created by wang jialei on 12-9-18.
//
//

#import "show_img_ViewController.h"

@interface show_img_ViewController ()

@end

@implementation show_img_ViewController
@synthesize scrollView;
@synthesize img=_img;

-(void)setImg:(UIImage *)img{
    _img = img;
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    UIImageView *imgView = [[UIImageView alloc] initWithFrame:CGRectMake(0, 0, 320, _img.size.height*320/_img.size.width)];
    [imgView setImage:_img];
    self.scrollView.contentSize = CGSizeMake(320, _img.size.height*320/_img.size.width);
    [self.scrollView addSubview:imgView];
    
    CGRect button_frame = CGRectMake(303, 0, 17, 17);
    UIButton *closeButton = [[UIButton alloc] initWithFrame:button_frame];
    
    [closeButton setBackgroundImage:[UIImage imageNamed:@"close-popup.png"] forState:UIControlStateNormal];
    //[closeButton addTarget:self action:@selector(close:)   forControlEvents:UIControlEventTouchUpInside];
    [closeButton addTarget:self action:@selector(close:) forControlEvents:UIControlEventTouchUpInside];
    [self.view addSubview:closeButton];
	// Do any additional setup after loading the view.
}

- (void)viewDidUnload
{
    [self setScrollView:nil];
    [self setImg:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (void)close:(id)sender {
    [self dismissModalViewControllerAnimated:YES];
}
@end
